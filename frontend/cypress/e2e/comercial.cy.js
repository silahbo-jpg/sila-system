describe('Licença Comercial', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173/login');
    cy.get('input[placeholder="Usuário"]').type('admin');
    cy.get('input[placeholder="Senha"]').type('admin123');
    cy.contains('Entrar').click();
    cy.url().should('include', '/dashboard');
  });

  it('Deve acessar o formulário, preencher e submeter', () => {
    cy.contains('Comercial').click();
    cy.url().should('include', '/comercial');
    cy.get('input[name="nome_empresa"]').type('Empresa Teste');
    cy.get('input[name="nif"]').type('123456789');
    cy.get('form').submit();
    cy.contains('Licença criada com sucesso');
  });
});

