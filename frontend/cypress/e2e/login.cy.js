describe('Login e acesso protegido', () => {
  it('Deve autenticar e acessar dashboard', () => {
    cy.visit('http://localhost:5173/login');
    cy.get('input[placeholder="Usuário"]').type('admin');
    cy.get('input[placeholder="Senha"]').type('admin123');
    cy.contains('Entrar').click();
    cy.url().should('include', '/dashboard');
    cy.contains('Dashboard SILA-HBO');
  });
});

