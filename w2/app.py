from flask import Flask, jsonify

from container import ServicesContainer


def create_app():
    app = Flask(__name__)

    from repo.in_memory_user_repo import InMemoryUserRepo
    from repo.in_memory_task_repo import InMemoryTaskRepo
    from service.user import UserService
    from service.task import TaskService

    user_repo = InMemoryUserRepo()
    task_repo = InMemoryTaskRepo()
    user_service = UserService(user_repo)
    task_service = TaskService(task_repo, user_service)

    app.extensions["services_container"] = ServicesContainer(
        user_service=user_service,
        task_service=task_service,
    )

    from routes.user import users_blueprint
    from routes.task import tasks_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(tasks_blueprint)

    @app.get("/status")
    def status():
        return jsonify({"status": "ok"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
