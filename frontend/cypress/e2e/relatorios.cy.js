describe('Relatórios - Exportação', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173/login');
    cy.get('input[placeholder="Usuário"]').type('admin');
    cy.get('input[placeholder="Senha"]').type('admin123');
    cy.contains('Entrar').click();
    cy.url().should('include', '/dashboard');
  });

  it('Deve acessar relatórios e exportar CSV', () => {
    cy.contains('Relatórios').click();
    cy.url().should('include', '/relatorios');
    cy.contains('Exportar CSV').click();
    cy.contains('Arquivo CSV exportado');
  });

  it('Deve acessar relatórios e exportar PDF', () => {
    cy.contains('Relatórios').click();
    cy.url().should('include', '/relatorios');
    cy.contains('Exportar PDF').click();
    cy.contains('Arquivo PDF exportado');
  });
});

