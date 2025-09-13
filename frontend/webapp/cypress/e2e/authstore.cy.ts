/// <reference types="cypress" />

describe('Auth Store', () => {
  it('deve persistir token após login', () => {
    cy.visit('/login');
    cy.get('input[type=email], input[name=email]').type('demo@demo.com');
    cy.get('input[type=password], input[name=password]').type('SenhaRobustaInstitucional!');
    cy.get('button[type=submit], button').contains(/entrar|login/i).click();
    cy.window().then(win => {
      expect(win.localStorage.getItem('auth:accessToken')).to.exist;
      expect(win.localStorage.getItem('auth:refreshToken')).to.exist;
    });
  });
});

