
document.addEventListener("DOMContentLoaded", function () {
    // Function to send a PUT request to update the task title

    function updateTaskTitle(taskId, newTitle) {
        const url = `/api/tasks/${taskId}`;
        const data = {
            title: newTitle
        };

        fetch(url, {
            method: 'PUT',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Handle the successful response if needed
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Function to send a request to delete a task
    function deleteTask(taskId) {
        const url = `/api/tasks/${taskId}`;
        fetch(url, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                // Task deleted successfully, you can handle this as needed
                console.log('Task deleted successfully');
                location.reload();
            } else {
                // Handle error, such as task not found or deletion failed
                console.error('Task deletion failed');
            }
        })
        .catch(error => {
            // Handle network errors
            console.error('Network error:', error);
        });
    }

      // Function to add a subtask
      function addSubtask(parentTaskId, subtaskTitle) {
        const url = `/api/add_subtask/${parentTaskId}`;
        const data = {
            title: subtaskTitle
        };

        fetch(url, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.ok) {
                // Subtask added successfully
                console.log('Subtask added successfully');
                location.reload();
            } else {
                // Handle error, such as validation or addition failure
                console.error('Subtask addition failed');
            }
        })
        .catch(error => {
            // Handle network errors
            console.error('Network error:', error);
        });
    }

    const toggleButtons = document.querySelectorAll('.toggle-subtask-form');

    toggleButtons.forEach(toggleButton => {
        toggleButton.addEventListener('click', () => {
            console.log("clicked")
            const subtaskForm = toggleButton.nextElementSibling; // Get the form next to the button
            if (subtaskForm) {
                console.log('Subtask form found');
                subtaskForm.classList.toggle('hidden');
            } else {
                console.error('Subtask form not found');
            subtaskForm.classList.toggle('hidden'); // Toggle the form's visibility
        };
    });
});

    // JavaScript to handle "Edit" button clicks
    const editButtons = document.querySelectorAll('.edit-task');
    const taskTitles = document.querySelectorAll('.task h2, .subtask h3, .subsubtask h4');
    const deleteButtons = document.querySelectorAll('.delete-task');
    const addSubtaskButtons = document.querySelectorAll('.add-subtask');


    deleteButtons.forEach(deleteButton => {
        deleteButton.addEventListener('click', (event) => {
            event.stopPropagation(); 
            const taskId = deleteButton.dataset.taskId;
            if (confirm('Are you sure you want to delete this task?')) {
                // User confirmed, send a request to the server to delete the task
                deleteTask(taskId); // Implement this function
            }
        });
    });

    editButtons.forEach((editButton, index) => {
        console.log("editing")
        editButton.addEventListener('click', () => {
            // Create an input field for editing
            const inputField = document.createElement('input');
            inputField.type = 'text';
            inputField.value = taskTitles[index].textContent;
            
            // Create a "Save" button
            const saveButton = document.createElement('button');
            saveButton.textContent = 'Save';

            // Create a "Cancel" button
            const cancelButton = document.createElement('button');
            cancelButton.textContent = 'Cancel';

            // Replace the task title with the input field
            const titleElement = taskTitles[index];
            titleElement.innerHTML = '';
            titleElement.appendChild(inputField);
            titleElement.appendChild(saveButton);
            titleElement.appendChild(cancelButton);

            // Disable the "Edit" button
            //editButton.disabled = true;

            // Add a click event listener for the "Save" button
            saveButton.addEventListener('click', () => {
                const newTitle = inputField.value;
                if (newTitle.trim() !== '') {
                    // Update the task title in the DOM
                    taskTitles[index].textContent = newTitle;
                    // Implement the function to send the updated title to the server
                    const taskId = editButton.dataset.taskId;
                    updateTaskTitle(taskId, newTitle); // Implement this function

                    // Remove the input field and buttons
                    titleElement.innerHTML = newTitle;

                    // Enable the "Edit" button
                    editButton.disabled = false;
                }
                console.log("Debug information:", editButtons, taskTitles, deleteButtons, addSubtaskButtons);
            });

            // Add a click event listener for the "Cancel" button
            cancelButton.addEventListener('click', () => {
                // Remove the input field and buttons without making changes
                titleElement.innerHTML = taskTitles[index].textContent;

                // Enable the "Edit" button
                editButton.disabled = false;
            });
        });
    });

    // Get the form and select element
    const form = document.getElementById('move-task-form');

    if (form) {
        const select = form.querySelector('select');

        // Add an event listener to the form for submission
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            // Get the selected list_id from the <select> element
            const list_id = select.value;

            // Get the task_id from the hidden input field
            const task_id = document.querySelector('input[name="task_id"]').value;

            // Construct the URL
            const url = `/move_task/${task_id}/${list_id}`;

            // Create a fetch request with POST method
            fetch(url, {
                method: 'POST'
            })
            .then(response => {
                if (response.ok) {
                    location.reload()
                } else {
                    // Handle errors
                }
            })
            .catch(error => {
                // Handle network errors
                console.error('Network error:', error);
        });
    });
}
});