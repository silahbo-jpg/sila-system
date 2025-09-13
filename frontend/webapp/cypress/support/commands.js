Cypress.Commands.add('login', () => {
    cy.request('POST', 'http://localhost:8000/api/auth/login', {
      username: 'admin',
      password: 'admin123'
    }).then((response) => {
      expect(response.status).to.eq(200)
      window.localStorage.setItem('token', response.body.access_token)
    })
  })
  

