/// <reference types="cypress" />

describe('Catálogo de Serviços', () => {
  beforeEach(() => {
    // Login via UI
    cy.visit('/login');
    cy.get('input[type=email], input[name=email]').type('demo@demo.com');
    cy.get('input[type=password], input[name=password]').type('SenhaRobustaInstitucional!');
    cy.get('button[type=submit], button').contains(/entrar|login/i).click();
    cy.url().should('include', '/dashboard');
  });

  it('deve acessar a lista de serviços e visualizar detalhes', () => {
    cy.contains(/catálogo de serviços/i).click();
    cy.url().should('include', '/servicos');
    cy.get('ul').should('exist');
    cy.get('li').should('have.length.greaterThan', 0);
    cy.get('a').contains(/acessar/i).first().click();
    cy.url().should('match', /\/servicos\//);
    cy.contains(/serviço/i);
  });
});

