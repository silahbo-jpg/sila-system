describe('Cidadania - Cadastro de Cidadão', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173/login');
    cy.get('input[placeholder="Usuário"]').type('admin');
    cy.get('input[placeholder="Senha"]').type('admin123');
    cy.contains('Entrar').click();
    cy.url().should('include', '/dashboard');
  });

  it('Deve acessar a página de cidadania e cadastrar cidadão', () => {
    cy.contains('Cidadania').click();
    cy.url().should('include', '/cidadania');
    cy.get('input[name="nome"]').type('João Teste');
    cy.get('input[name="cpf"]').type('12345678901');
    cy.get('form').submit();
    cy.contains('Cidadão cadastrado com sucesso');
  });
});

