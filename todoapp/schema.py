import graphene
from graphene_django import DjangoObjectType
from .models import Todo
from users.models import CustomUser


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'detail', 'is_important',
                  'is_completed', 'created_at', 'completed_at')


class Query(graphene.ObjectType):
    all_todos = graphene.List(TodoType)
    all_active_todos = graphene.List(TodoType)
    all_completed_todos = graphene.List(TodoType)
    todo_by_id = graphene.Field(TodoType, id=graphene.Int(required=True))

    # get all todos
    def resolve_all_todos(root, info):
        return Todo.objects.filter(user=info.context.user)

    # get all active todos
    def resolve_all_active_todos(root, info):
        return Todo.active.filter(user=info.context.user)

    # get all completed todos
    def resolve_all_completed_todos(root, info):
        return Todo.completed.filter(user=info.context.user)

    # get single todo by id
    def resolve_todo_by_id(root, info, id):
        return Todo.objects.get(user=info.context.user, pk=id)


class CreateTodoMutation(graphene.Mutation):
    '''
    Create new todo
    '''
    todo = graphene.Field(TodoType)
    ok = graphene.Boolean()

    class Arguments:
        title = graphene.String(required=True)
        detail = graphene.String()
        is_important = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):  # title, detail, is_important):
        # todo = Todo(title=title, detail=detail, is_important=is_important)
        print(kwargs)
        todo = Todo()
        for key, value in kwargs.items():
            setattr(todo, key, value)
        todo.owner = info.context.user
        todo.save()
        ok = True
        return CreateTodoMutation(todo=todo, ok=ok)


class UpdateTodoMutation(graphene.Mutation):
    '''
    Update todo using id
    '''
    todo = graphene.Field(TodoType)
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        detail = graphene.String()
        is_important = graphene.Boolean()
        is_completed = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id, title, detail, is_important, is_completed):
        todo = Todo.objects.get(id=id, owner=info.context.user)
        todo.title = title
        todo.detail = detail
        todo.is_important = is_important
        todo.is_completed = is_completed
        todo.save()
        ok = True
        return UpdateTodoMutation(todo=todo, ok=ok)


class DeleteTodoMutation(graphene.Mutation):
    '''
    Delete todo using id
    '''
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    def mutate(cls, root, info, id):
        todo = Todo.objects.get(id=id, owner=info.context.user)
        todo.delete()
        ok = True
        return DeleteTodoMutation(ok=ok)


class Mutation(graphene.ObjectType):
    create_todo = CreateTodoMutation.Field()
    update_todo = UpdateTodoMutation.Field()
    delete_todo = DeleteTodoMutation.Field()
