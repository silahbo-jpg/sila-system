describe('Permissões de acesso por cargo', () => {
  it('Sidebar: atendente só vê Cidadania', () => {
    cy.visit('http://localhost:5173/login');
    cy.get('input[placeholder="Usuário"]').type('atendente');
    cy.get('input[placeholder="Senha"]').type('atendente123');
    cy.contains('Entrar').click();
    cy.url().should('include', '/dashboard');
    cy.get('aside').within(() => {
      cy.contains('Cidadania').should('exist');
      cy.contains('Comercial').should('not.exist');
      cy.contains('Sanitário').should('not.exist');
      cy.contains('Estatísticas').should('not.exist');
      cy.contains('Relatórios').should('not.exist');
      cy.contains('Justiça').should('not.exist');
    });
  });
});

