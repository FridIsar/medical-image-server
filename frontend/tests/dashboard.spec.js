import { test, expect } from '@playwright/test';

const baseUrl = process.env.VITE_BASE_URL || 'http://localhost:5173';

test.describe('Dashboard Page', () => {
  test.beforeEach(async ({ page }) => {
    // Log in before each test
    await page.goto(`${baseUrl}/login`, { waitUntil: 'networkidle' });
    await page.fill('input[placeholder="Username"]', 'user');
    await page.fill('input[placeholder="Password"]', 'password');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(`${baseUrl}/dashboard`);
  });

  test('should display patient name when button is clicked', async ({ page }) => {
    // Click the button to display patient name
    await page.click('button:text("Display Patient Name")');

    // Wait for the patient name to be displayed
    await expect(page.locator('text=Patient Name:')).toBeVisible();

    // Check that the patient name is correct
    const patientName = await page.textContent('#patient-name');
    expect(patientName).toBe('Patient Name: PatientName');
  });

  test('should display middle slice image when button is clicked', async ({ page }) => {
    // Click the button to display the image
    await page.click('button:text("Display Image")');

    // Wait for the canvas to be visible
    await expect(page.locator('canvas')).toBeVisible();
  });

  test('should log out successfully', async ({ page }) => {
    // Click the logout button
    await page.click('button:text("Logout")');

    // Ensure we're redirected to the login page
    await expect(page).toHaveURL(`${baseUrl}/login`);
  });
});
