set -e

IMAGE_NAME="tarea-3-cph-portfolio"
CONTAINER_NAME="tarea-3-cph-portfolio"
PORT=8084

echo "=== Portfolio Docker Deployment ==="

# Stop and remove existing container if running
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Stopping existing container..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
fi

# Build the image (run from script directory, parent of webpage)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Building Docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" .

echo "Creating and starting container: $CONTAINER_NAME"
docker run -d \
    --name "$CONTAINER_NAME" \
    -p "$PORT:80" \
    "$IMAGE_NAME"

echo ""
echo "=== Deployment complete ==="
echo "Site is available at: http://localhost:$PORT"
echo ""
echo "Useful commands:"
echo "  View logs:    docker logs -f $CONTAINER_NAME"
echo "  Stop:        docker stop $CONTAINER_NAME"
echo "  Remove:      docker rm $CONTAINER_NAME"
