from app import app
import k8s_connection
import _thread
if __name__ == "__main__":
    k8s_connection.k8sInitial()
    _thread.start_new_thread(k8s_connection.list_deployment_for_all_namespaces,())
    app.run(debug=True,port=5000)
