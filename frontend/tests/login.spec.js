import { test, expect } from '@playwright/test';

test.describe('Login Page', () => {
  
  // Test to check that the login form displays correctly
  test('should display login form', async ({ page }) => {
    await page.goto('/login');
    await expect(page.locator('input[placeholder="Username"]')).toBeVisible();
    await expect(page.locator('input[placeholder="Password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  // Test for successful login and redirect to the dashboard
  test('should successfully log in with correct credentials', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[placeholder="Username"]', 'testuser');
    await page.fill('input[placeholder="Password"]', 'testpass');
    await page.click('button[type="submit"]');
    
    // After successful login, we expect a redirect to /dashboard
    await expect(page).toHaveURL('/dashboard');
  });

  // Test for failed login attempt
  test('should show error with incorrect credentials', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[placeholder="Username"]', 'wronguser');
    await page.fill('input[placeholder="Password"]', 'wrongpass');
    await page.click('button[type="submit"]');
    
    // We expect an error message to be displayed
    await expect(page.locator('text=Login failed')).toBeVisible();
  });
});
