document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('event-form'); 
    form.addEventListener('submit', handleSubmit);
  });
  
  function handleSubmit(event) {
    event.preventDefault(); // Prevent the default form submission
  
    // Get the data from the form
    const eventDate = document.getElementById('event-date').value; 
    const city = document.getElementById('city').value; // Ensure this ID matches your input's ID
  
    // Send the data to the server using AJAX
    $.ajax({
      url: 'http://localhost:8080/findEvents', // Ensure this matches your Flask app's endpoint
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ date: eventDate, city: city }),
      success: function(response) {
        // If successful, store the response in localStorage and redirect to events.html
        localStorage.setItem('eventResponse', JSON.stringify(response));
        window.location.href = 'events.html';
      },
      error: function(xhr, status, error) {
        // If there's an error, log it to the console
        console.error('Error:', status, error);
      }
    });
  }
  
