let login = Math.random().toString(36).substring(2, 15);

describe('Register', function() {
  it('visit bibliohub', function () {
    cy.visit('http://localhost:8081/')
  });

  it('click Sign Up', function () {
    cy.contains('Sign up').click();
  });

  it('enter email', function () {
    cy.get('#reg_email').type('test@mail.com');
  });

  it('enter login', function () {
    cy.get('#reg_login').type(login);
  });

  it('enter password', function () {
    cy.get('#reg_password').type('pass');
  });

  it('click register', function () {
    cy.contains('Register').click();
  });
});

describe('Login', function() {
  it('enter login', function () {
    cy.get('#login').type(login);
  });

  it('enter password', function () {
    cy.get('#password').type('pass');
  });

  it('click sign in', function () {
    cy.get('.btn-dark').click();
  });

  it('check current url', function () {
    cy.url().should('eq', 'http://localhost:8081/#/hub')
  });
});

describe('Logout and login', function() {
  it('logout', function () {
    cy.contains('Log out').click();
  });

  it('login', function () {
    cy.get('#login').type(login);
    cy.get('#password').type('pass');
    cy.get('.btn-dark').click();
  });

  it('check current url', function () {
    cy.url().should('eq', 'http://localhost:8081/#/hub')
  });
});

describe('Add a new book', function() {
  it('open add book popup', function () {
    cy.contains('Add Book').click();
  });

  it('enter title', function () {
    cy.get('#form-title-input')
      .type('Sapiens, A Brief History of Humankind');
  });

  it('enter author', function () {
    cy.get('#form-author-input')
      .type('Yuval Noah Harari');
  });

  it('enter year', function () {
    cy.get('#form-year-input')
      .type(2011);
  });

  it('add file', function () {
    cy.uploadFile('pdf/start_projektu.pdf', 'input[type=file]', 'application/pdf');
  });

  it('submit the new book', function () {
    cy.contains('Submit').click();
  });
});

describe('Add new file', function() {
  it('open add book popup', function () {
    cy.contains('Add pdf').click();
  });

  it('add file', function () {
    cy.uploadFile('pdf/przepis.pdf', 'input#form-file-input.custom-file-input', 'application/pdf');
  });

  it('submit the new file', function () {
    cy.contains('Update').click();
  });
});

describe('Add new book', function() {
  it('open add book popup', function () {
    cy.contains('Add Book').click();
  });

  it('enter title', function () {
    cy.get('#form-title-input')
      .type('Homo Deus: A Brief History of Tomorrow');
  });

  it('enter author', function () {
    cy.get('#form-author-input')
      .type('Yuval Noah Harari');
  });

  it('enter year', function () {
    cy.get('#form-year-input')
      .type(2016);
  });

  it('add file', function () {
    cy.uploadFile('pdf/start_projektu.pdf', 'input[type=file]', 'application/pdf');
  });

  it('submit the new book', function () {
    cy.contains('Submit').click();
  });
});

describe('Download files', function() {
  it('download 2 files', function () {
    cy.contains('przepis.pdf').click();
    cy.contains('start_projektu.pdf').click();
  });
});

describe('Delete file', function() {
  it('click on trash', function () {
    cy.get('[data-cy=trash]').first().click();
  });
});

describe('Delete a book', function() {
  it('click on delete', function () {
    cy.contains('Delete').click();
  });
});
