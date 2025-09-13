describe('Sanitário - Emissão de Certidão', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173/login');
    cy.get('input[placeholder="Usuário"]').type('admin');
    cy.get('input[placeholder="Senha"]').type('admin123');
    cy.contains('Entrar').click();
    cy.url().should('include', '/dashboard');
  });

  it('Deve acessar a página sanitária e emitir certidão', () => {
    cy.contains('Sanitário').click();
    cy.url().should('include', '/sanitario');
    cy.get('input[name="nome_estabelecimento"]').type('Estabelecimento Teste');
    cy.get('input[name="cnpj"]').type('12345678000199');
    cy.get('form').submit();
    cy.contains('Certidão emitida com sucesso');
  });
});

