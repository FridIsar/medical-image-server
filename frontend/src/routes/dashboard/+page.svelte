<script>
    import { tick } from 'svelte';

    let patientName = '';
    let imageData = '';
    let error = '';
    let canvas;
    let ctx;
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
          imageData = data.image;
          // Initialize canvas after image data is available and rendered
          await tick();  // Wait for the DOM to update (using svelte's tick function)
          renderImage(imageData);
        } else {
          error = 'Failed to fetch image';
        }
      } catch (e) {
        error = 'An error occurred while fetching image';
        console.error(e);
      }
    }
  
    function renderImage(imageArray) {
      const width = imageArray[0].length;
      const height = imageArray.length;
  
      // Ensure the canvas context is available
      if (canvas) {
        ctx = canvas.getContext('2d');
        const imageData = ctx.createImageData(width, height);
        let index = 0;
  
        for (let y = 0; y < height; y++) {
          for (let x = 0; x < width; x++) {
            const pixelValue = imageArray[y][x];
            imageData.data[index++] = pixelValue; // R
            imageData.data[index++] = pixelValue; // G
            imageData.data[index++] = pixelValue; // B
            imageData.data[index++] = 255;        // A
          }
        }
  
        ctx.putImageData(imageData, 0, 0);
      } else {
        error = 'Canvas element not found';
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
    <canvas bind:this={canvas} width="512" height="512"></canvas>
  {/if}
  
  {#if error}
    <p>{error}</p>
  {/if}
  