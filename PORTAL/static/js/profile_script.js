document.getElementById('subscription').addEventListener('click', function() {
    fetch('/profile/subscription/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(data => {
        document.getElementById('modal-body').innerHTML = data;
        document.getElementById('modal').style.display = 'block'; 

        const form = document.querySelector('form');
        form.addEventListener('submit', function(event) {
            event.preventDefault(); 
            const formData = new FormData(form);

            fetch('/profile/subscription/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json(); 
            })
            .then(data => {
                const alertMessage = document.getElementById('alert-message-partial');
                alertMessage.style.display = 'block'; 
                if(data.success) {
                    alertMessage.className = 'alert alert-success';
                    alertMessage.innerText = data.message; 
                } else {
                    alertMessage.className = 'alert alert-danger';
                    alertMessage.innerText = data.message;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('alert-message').style.display = 'none'; 
});

window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        modal.style.display = 'none';
        document.getElementById('alert-message').style.display = 'none';
    }
};