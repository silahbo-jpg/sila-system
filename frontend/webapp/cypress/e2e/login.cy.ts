/// <reference types="cypress" />

describe('Login Flow', () => {
  it('should show login page and allow user login', () => {
    cy.visit('/login');
    cy.get('input[type=email], input[name=email]').type('demo@demo.com');
    cy.get('input[type=password], input[name=password]').type('SenhaRobustaInstitucional!');
    cy.get('button[type=submit], button').contains(/entrar|login/i).click();
    cy.url().should('include', '/dashboard');
    cy.contains(/dashboard/i);
  });
});

// Ajuste o email/senha conforme o seed/demo do backend.

