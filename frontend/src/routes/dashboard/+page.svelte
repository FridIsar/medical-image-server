<script>
    import { onMount } from 'svelte';
    let patientName = '';
    let imageData = '';
    let error = '';
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  
    async function fetchPatientName() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_URL}/patient-name?dicom_filename=test/example.dcm`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
  
        if (response.ok) {
          const data = await response.json();
          patientName = data.patient_name;
        } else {
          error = 'Failed to fetch patient name';
        }
      } catch (e) {
        error = 'An error occurred while fetching patient name';
      }
    }
  
    async function fetchImage() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_URL}/middle-slice-image?dicom_filename=test/example.dcm`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
  
        if (response.ok) {
          const data = await response.json();
          imageData = JSON.stringify(data.image);
        } else {
          error = 'Failed to fetch image';
        }
      } catch (e) {
        error = 'An error occurred while fetching image';
      }
    }
  
    function logout() {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
  </script>
  
  <h1>Dashboard</h1>
  
  <button on:click={fetchPatientName}>Display Patient Name</button>
  <button on:click={fetchImage}>Display Image</button>
  <button on:click={logout}>Logout</button>
  
  {#if patientName}
    <p id="patient-name">Patient Name: {patientName}</p>
  {/if}
  
  {#if imageData}
    <p id="image-data">Image Data: {imageData}</p>
  {/if}
  
  {#if error}
    <p>{error}</p>
  {/if}
  