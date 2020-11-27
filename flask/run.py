from app import app
import k8s_connection
if __name__ == "__main__":
    k8s_connection.k8sInitial()
    app.run(debug=True,port=5000)
