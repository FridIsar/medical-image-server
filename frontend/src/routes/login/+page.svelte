<script>
    let username = '';
    let password = '';
    let error = '';
  
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  
    async function login() {
      try {
        const response = await fetch(`${API_URL}/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({ username, password }),
        });
  
        if (response.ok) {
          const data = await response.json();
          localStorage.setItem('token', data.access_token);
          // Redirect to the dashboard on successful login
          window.location.href = '/dashboard';
        } else {
          // Show error message if login fails
          error = 'Login failed';
        }
      } catch (e) {
        error = 'An error occurred';
      }
    }
  </script>
  
  <form on:submit|preventDefault={login}>
    <input type="text" bind:value={username} placeholder="Username" required />
    <input type="password" bind:value={password} placeholder="Password" required />
    <button type="submit">Login</button>
    {#if error}
      <p>{error}</p>
    {/if}
  </form>
  