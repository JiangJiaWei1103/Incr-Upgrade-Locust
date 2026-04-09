#!/usr/bin/env bash
set -euo pipefail

echo "Setting up environment for local incremental upgrade/rollback tests..."
echo ""

ROOT_DIR="${HOME}/Desktop/Fun/my_ray/kuberay"
cd "${ROOT_DIR}"
echo "Using ROOT_DIR=${ROOT_DIR}"

# Configure components.
KIND_VER="${KIND_VER:-v1.29.0}"
KIND_CLUSTER_NAME="${KIND_CLUSTER_NAME:-kind}"
# KIND_CONFIG="${KIND_CONFIG:-${ROOT_DIR}/ci/kind-config-buildkite-1-29.yml}"
ISTIO_VER="${ISTIO_VER:-1.28.3}"

echo "KIND_CLUSTER_NAME=${KIND_CLUSTER_NAME}"
# echo "KIND_CONFIG=${KIND_CONFIG}"

if ! command -v kind >/dev/null 2>&1; then
  echo "kind not found on PATH. Please install kind first."
  exit 1
fi

if ! command -v kubectl >/dev/null 2>&1; then
  echo "kubectl not found on PATH. Please install kubectl first."
  exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "curl not found on PATH. Please install curl first."
  exit 1
fi

echo "=== 1. Create kind cluster ==="
kind delete cluster --name "${KIND_CLUSTER_NAME}" || true
kind create cluster \
  --image "kindest/node:${KIND_VER}" \
  --name "${KIND_CLUSTER_NAME}" \
  --wait 900s
  # --config "${KIND_CONFIG}"

echo "=== 2. Install MetalLB for LoadBalancer IPs on kind ==="
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.12/config/manifests/metallb-native.yaml
kubectl wait \
  --namespace metallb-system \
  --for=condition=ready \
  pod \
  --selector=app=metallb \
  --timeout=90s
kubectl apply -f "${ROOT_DIR}/ray-operator/config/samples/gateway-api/metallb-config.yaml"

echo "=== 3. Install Gateway API CRDs (required for incremental upgrade) ==="
kubectl apply --server-side -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.1/standard-install.yaml

echo "=== 4. Install Istio (Gateway controller) and GatewayClass ==="
if [ ! -d "${ROOT_DIR}/istio-${ISTIO_VER}" ]; then
  curl -L https://istio.io/downloadIstio | ISTIO_VERSION="${ISTIO_VER}" sh -
fi
"${ROOT_DIR}/istio-${ISTIO_VER}/bin/istioctl" install --set profile=minimal -y

kubectl wait \
  --namespace istio-system \
  --for=condition=ready \
  pod \
  --selector=app=istiod \
  --timeout=120s

kubectl apply -f "${ROOT_DIR}/ray-operator/config/samples/gateway-api/istio-class.yaml"

echo "=== 5. Build and deploy KubeRay operator ==="
pushd "${ROOT_DIR}/ray-operator" >/dev/null

# In local runs, default to "not from ray release automation".
: "${IS_FROM_RAY_RELEASE_AUTOMATION:=0}"
export IS_FROM_RAY_RELEASE_AUTOMATION

source ../.buildkite/build-start-operator.sh
kubectl wait \
  --timeout=90s \
  --for=condition=Available=true \
  deployment kuberay-operator
popd >/dev/null

echo "=== Done ==="
