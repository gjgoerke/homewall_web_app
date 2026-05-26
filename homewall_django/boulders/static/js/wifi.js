// For button clicks on index page
async function lightBoulderFromButton(start, finish, general, feet, hands) {
    const button = event.target;
    const originalText = button.innerHTML;
    
    try {
        button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Lighting...';
        button.disabled = true;

        await updateLights(start, finish, general, feet, hands);
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to light boulder. Please try again.');
    } finally {
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

// For circle clicks on new page
async function lightBoulderFromCircle(start, finish, general, feet, hands) {
    try {
        await updateLights(start, finish, general, feet, hands);
    } catch (error) {
        console.error('Error in lightBoulderFromCircle:', error);
    }
}

// Shared lighting logic
async function updateLights(start, finish, general, feet, hands) {
    const holds = [
        ...start.map(index => ({index, type: 1})),
        ...finish.map(index => ({index, type: 2})),
        ...general.map(index => ({index, type: 3})),
        ...feet.map(index => ({index, type: 4})),
        ...hands.map(index => ({index, type: 5}))
    ];

    console.log('Sending holds:', holds);

    const response = await fetch('/api/lights/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ holds }),
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Success:', data);
    return data;
}