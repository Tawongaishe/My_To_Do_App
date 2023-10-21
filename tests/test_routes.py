import json
from unittest.mock import patch

#import the app factory 
from backend import create_app, db
app = create_app()


def test_get_list():
    with app.test_client() as client:
        # Make a GET request to /lists/1
        response = client.get('/lists/1')

        # Check that the response is successful and has the expected data
        assert response.status_code == 200
        assert json.loads(response.data) == {
            'id': 1,
            'title': 'My List',
            'tasks': [
                {'id': 1, 'title': 'Task 1', 'done': False},
                {'id': 2, 'title': 'Task 2', 'done': True},
            ],
        }


@patch('backend.routes.List.edit')
def test_edit_list(mock_edit):
    with app.test_client() as client:
        # Make a PUT request to /lists/1 with a new title
        response = client.put('/lists/1', json={'title': 'New Title'})

        # Check that the response is successful and the edit function was called
        assert response.status_code == 200
        assert json.loads(response.data) == {'message': 'List updated successfully'}
        mock_edit.assert_called_once_with('New Title')


@patch('backend.routes.List.delete')
def test_delete_list(mock_delete):
    with app.test_client() as client:
        # Make a DELETE request to /lists/1
        response = client.delete('/lists/1')

        # Check that the response is successful and the delete function was called
        assert response.status_code == 200
        assert json.loads(response.data) == {'message': 'List and associated tasks deleted successfully'}
        mock_delete.assert_called_once()