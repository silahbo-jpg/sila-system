import { rest } from 'msw';
import { server } from '../../../../test-utils/mockApi';
import { citizenshipApi } from '../citizenshipApi';
import { mockCitizenRequest, mockRequestsList } from '../../../../test-utils/mockApi';

describe('citizenshipApi', () => {
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());

  describe('getCitizenRequests', () => {
    it('should fetch citizen requests successfully', async () => {
      const response = await citizenshipApi.getCitizenRequests();
      expect(response).toEqual(mockRequestsList);
    });

    it('should handle API error', async () => {
      server.use(
        rest.get('http://localhost:8000/api/v1/citizenship/requests/', (req, res, ctx) => {
          return res(ctx.status(500), ctx.json({ message: 'Internal Server Error' }));
        })
      );

      await expect(citizenshipApi.getCitizenRequests()).rejects.toThrow('Request failed with status code 500');
    });
  });

  describe('getCitizenRequestById', () => {
    it('should fetch a single citizen request', async () => {
      const response = await citizenshipApi.getCitizenRequestById('1');
      expect(response).toEqual(mockCitizenRequest);
    });
  });

  describe('createCitizenRequest', () => {
    it('should create a new citizen request', async () => {
      const newRequest = {
        name: 'New User',
        nif: '111222333',
        birthDate: '1990-01-01',
        gender: 'M' as const,
        address: {
          street: 'New Street',
          city: 'New City',
          postalCode: '1234-567',
        },
        contact: {
          email: 'new@example.com',
          phone: '911222333',
        },
      };

      const response = await citizenshipApi.createCitizenRequest(newRequest);
      expect(response).toMatchObject({
        ...newRequest,
        id: 'new-request-id',
      });
    });
  });

  describe('updateCitizenRequest', () => {
    it('should update an existing citizen request', async () => {
      const updates = {
        name: 'Updated Name',
        contact: {
          email: 'updated@example.com',
        },
      };

      const response = await citizenshipApi.updateCitizenRequest('1', updates);
      expect(response).toMatchObject(updates);
    });
  });

  describe('submitCitizenRequest', () => {
    it('should submit a citizen request for review', async () => {
      const response = await citizenshipApi.submitCitizenRequest('1');
      expect(response.status).toBe('submitted');
    });
  });

  describe('deleteCitizenRequest', () => {
    it('should delete a citizen request', async () => {
      await expect(citizenshipApi.deleteCitizenRequest('1')).resolves.not.toThrow();
    });
  });
});

