# Full Stack Integration Workflow

## Purpose
Systematic approach to integrating frontend and backend components in full stack applications, ensuring seamless communication and data flow.

## Prerequisites
- Frontend application structure established
- Backend API endpoints defined and tested
- Database schema and models implemented
- Development environment configured

## Integration Planning Phase

### 1. API Contract Definition
```xml
<ask_followup_question>
<question>What type of API integration are we implementing?</question>
<options>["REST API with JSON", "GraphQL API", "WebSocket/Real-time", "Mixed API Types"]</options>
</ask_followup_question>
```

#### Define API Contracts
- **Endpoint Documentation**: Document all API endpoints with request/response formats
- **Data Transfer Objects**: Define consistent data structures between frontend/backend
- **Error Handling**: Establish error response formats and handling strategies
- **Authentication Flow**: Define authentication and authorization mechanisms

```typescript
// Example API contract definition
interface ApiResponse<T> {
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: Record<string, string[]>;
  };
  timestamp: string;
}

interface User {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  createdAt: string;
}

interface CreateUserRequest {
  email: string;
  firstName: string;
  lastName: string;
  password: string;
}
```

### 2. Data Flow Architecture
```xml
<read_file>
<path>frontend/src/services</path>
</read_file>
```

Analyze and plan:
- **State Management**: How frontend state will be managed and synchronized
- **Caching Strategy**: Client-side caching of API responses
- **Real-time Updates**: WebSocket or polling for live data
- **Offline Handling**: How the app behaves when offline

## Frontend Integration Implementation

### 3. API Service Layer
Create centralized API service layer:

```typescript
// services/api.ts
class ApiService {
  private baseURL: string;
  private defaultHeaders: Record<string, string>;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    const config: RequestInit = {
      headers: { ...this.defaultHeaders, ...options.headers },
      ...options,
    };

    // Add authentication token if available
    const token = this.getAuthToken();
    if (token) {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${token}`,
      };
    }

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new ApiError(response.status, data.error?.message || 'Request failed', data.error);
      }

      return data;
    } catch (error) {
      if (error instanceof ApiError) throw error;
      throw new ApiError(0, 'Network error or request failed');
    }
  }

  // User management methods
  async getUsers(): Promise<ApiResponse<User[]>> {
    return this.request<User[]>('/api/v1/users');
  }

  async createUser(userData: CreateUserRequest): Promise<ApiResponse<User>> {
    return this.request<User>('/api/v1/users', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async updateUser(id: number, userData: Partial<User>): Promise<ApiResponse<User>> {
    return this.request<User>(`/api/v1/users/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(userData),
    });
  }

  private getAuthToken(): string | null {
    // Implementation depends on your auth strategy
    return localStorage.getItem('authToken');
  }
}

class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export const apiService = new ApiService(process.env.REACT_APP_API_URL || 'http://localhost:5000');
```

### 4. State Management Integration
```typescript
// stores/userStore.ts (example with Zustand)
import { create } from 'zustand';
import { apiService } from '../services/api';

interface UserState {
  users: User[];
  loading: boolean;
  error: string | null;
  fetchUsers: () => Promise<void>;
  createUser: (userData: CreateUserRequest) => Promise<void>;
  updateUser: (id: number, userData: Partial<User>) => Promise<void>;
}

export const useUserStore = create<UserState>((set, get) => ({
  users: [],
  loading: false,
  error: null,

  fetchUsers: async () => {
    set({ loading: true, error: null });
    try {
      const response = await apiService.getUsers();
      set({ users: response.data || [], loading: false });
    } catch (error) {
      set({ 
        error: error instanceof ApiError ? error.message : 'Failed to fetch users',
        loading: false 
      });
    }
  },

  createUser: async (userData) => {
    set({ loading: true, error: null });
    try {
      const response = await apiService.createUser(userData);
      if (response.data) {
        set(state => ({ 
          users: [...state.users, response.data!],
          loading: false 
        }));
      }
    } catch (error) {
      set({ 
        error: error instanceof ApiError ? error.message : 'Failed to create user',
        loading: false 
      });
    }
  },

  updateUser: async (id, userData) => {
    set({ loading: true, error: null });
    try {
      const response = await apiService.updateUser(id, userData);
      if (response.data) {
        set(state => ({
          users: state.users.map(user => 
            user.id === id ? { ...user, ...response.data } : user
          ),
          loading: false
        }));
      }
    } catch (error) {
      set({ 
        error: error instanceof ApiError ? error.message : 'Failed to update user',
        loading: false 
      });
    }
  },
}));
```

### 5. Component Integration
```typescript
// components/UserList.tsx
import React, { useEffect } from 'react';
import { useUserStore } from '../stores/userStore';

export const UserList: React.FC = () => {
  const { users, loading, error, fetchUsers } = useUserStore();

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  if (loading) return <div>Loading users...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Users</h2>
      {users.length === 0 ? (
        <p>No users found</p>
      ) : (
        <ul>
          {users.map(user => (
            <li key={user.id}>
              {user.firstName} {user.lastName} ({user.email})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
```

## Backend Integration Implementation

### 6. CORS Configuration
```python
# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Configure CORS for frontend integration
    CORS(app, 
         origins=['http://localhost:3000', 'https://yourdomain.com'],
         methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
         allow_headers=['Content-Type', 'Authorization'],
         supports_credentials=True)
    
    return app
```

### 7. Response Serialization
```python
# backend/app/utils/serializers.py
from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True, format='iso')

class ApiResponseSchema(Schema):
    data = fields.Raw(allow_none=True)
    message = fields.Str(allow_none=True)
    timestamp = fields.DateTime(format='iso', dump_default=datetime.utcnow)

def create_api_response(data=None, message=None, status_code=200):
    """Create standardized API response"""
    response_data = ApiResponseSchema().dump({
        'data': data,
        'message': message
    })
    return response_data, status_code
```

### 8. Error Handling Integration
```python
# backend/app/utils/error_handlers.py
from flask import jsonify
from marshmallow import ValidationError

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    response = {
        'error': {
            'code': 'VALIDATION_ERROR',
            'message': 'Invalid input data',
            'details': error.messages
        },
        'timestamp': datetime.utcnow().isoformat()
    }
    return jsonify(response), 400

@app.errorhandler(404)
def handle_not_found(error):
    response = {
        'error': {
            'code': 'RESOURCE_NOT_FOUND',
            'message': 'Resource not found'
        },
        'timestamp': datetime.utcnow().isoformat()
    }
    return jsonify(response), 404
```

## Real-time Integration

### 9. WebSocket Integration
```python
# backend/app/socket_handlers.py
from flask_socketio import emit, join_room, leave_room
from app.utils.auth import verify_socket_token

@socketio.on('connect')
def handle_connect(auth):
    token = auth.get('token') if auth else None
    if not token:
        return False
    
    try:
        user_data = verify_socket_token(token)
        session['user_id'] = user_data['user_id']
        join_room(f"user_{user_data['user_id']}")
        emit('connected', {'message': 'Connected successfully'})
    except Exception:
        return False

@socketio.on('subscribe_to_updates')
def handle_subscribe(data):
    if 'user_id' not in session:
        emit('error', {'message': 'Authentication required'})
        return
    
    update_type = data.get('type')
    if update_type == 'user_updates':
        join_room('user_updates')
        emit('subscribed', {'type': update_type})

def broadcast_user_update(user_data):
    """Broadcast user updates to subscribed clients"""
    socketio.emit('user_updated', user_data, room='user_updates')
```

```typescript
// frontend/src/services/websocket.ts
import io, { Socket } from 'socket.io-client';

class WebSocketService {
  private socket: Socket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  connect(token: string): void {
    this.socket = io(process.env.REACT_APP_WS_URL || 'http://localhost:5000', {
      auth: { token },
      transports: ['websocket']
    });

    this.socket.on('connect', () => {
      console.log('Connected to WebSocket');
      this.reconnectAttempts = 0;
    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket');
      this.handleReconnect();
    });

    this.socket.on('user_updated', (userData) => {
      // Update local state or trigger refresh
      this.handleUserUpdate(userData);
    });
  }

  subscribeToUserUpdates(): void {
    if (this.socket) {
      this.socket.emit('subscribe_to_updates', { type: 'user_updates' });
    }
  }

  private handleUserUpdate(userData: User): void {
    // Integrate with your state management
    useUserStore.getState().updateUserFromSocket(userData);
  }

  private handleReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      setTimeout(() => {
        this.reconnectAttempts++;
        this.socket?.connect();
      }, 1000 * Math.pow(2, this.reconnectAttempts));
    }
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }
}

export const wsService = new WebSocketService();
```

## Testing Integration

### 10. Integration Tests
```python
# backend/tests/test_integration.py
import pytest
import json
from app import create_app, db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

class TestUserAPIIntegration:
    def test_full_user_workflow(self, client):
        # Create user
        user_data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'password123'
        }
        
        response = client.post('/api/v1/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        created_user = response.json['data']
        assert created_user['email'] == user_data['email']
        
        # Get users list
        response = client.get('/api/v1/users')
        assert response.status_code == 200
        assert len(response.json['data']) == 1
        
        # Update user
        update_data = {'first_name': 'Updated'}
        response = client.patch(f"/api/v1/users/{created_user['id']}",
                               data=json.dumps(update_data),
                               content_type='application/json')
        
        assert response.status_code == 200
        assert response.json['data']['first_name'] == 'Updated'
```

```typescript
// frontend/src/__tests__/integration.test.ts
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserList } from '../components/UserList';
import { apiService } from '../services/api';

// Mock API service
jest.mock('../services/api');
const mockApiService = apiService as jest.Mocked<typeof apiService>;

describe('User Integration Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('displays users from API', async () => {
    const mockUsers = [
      { id: 1, email: 'test@example.com', firstName: 'Test', lastName: 'User', createdAt: '2024-01-01T00:00:00Z' }
    ];

    mockApiService.getUsers.mockResolvedValue({
      data: mockUsers,
      timestamp: '2024-01-01T00:00:00Z'
    });

    render(<UserList />);

    await waitFor(() => {
      expect(screen.getByText('Test User (test@example.com)')).toBeInTheDocument();
    });

    expect(mockApiService.getUsers).toHaveBeenCalledTimes(1);
  });

  test('handles API errors gracefully', async () => {
    mockApiService.getUsers.mockRejectedValue(new ApiError(500, 'Server error'));

    render(<UserList />);

    await waitFor(() => {
      expect(screen.getByText(/Error: Server error/)).toBeInTheDocument();
    });
  });
});
```

## Performance Optimization

### 11. Caching Strategy
```typescript
// frontend/src/utils/cache.ts
class ApiCache {
  private cache = new Map<string, { data: any; timestamp: number; ttl: number }>();

  set(key: string, data: any, ttl: number = 300000): void { // 5 minutes default
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl
    });
  }

  get(key: string): any | null {
    const item = this.cache.get(key);
    if (!item) return null;

    if (Date.now() - item.timestamp > item.ttl) {
      this.cache.delete(key);
      return null;
    }

    return item.data;
  }

  invalidate(pattern: string): void {
    for (const key of this.cache.keys()) {
      if (key.includes(pattern)) {
        this.cache.delete(key);
      }
    }
  }
}

export const apiCache = new ApiCache();
```

### 12. Request Optimization
```typescript
// services/optimizedApi.ts
class OptimizedApiService extends ApiService {
  private requestQueue = new Map<string, Promise<any>>();

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    // Deduplicate identical requests
    const requestKey = `${options.method || 'GET'}-${endpoint}-${JSON.stringify(options.body || {})}`;
    
    if (this.requestQueue.has(requestKey)) {
      return this.requestQueue.get(requestKey);
    }

    // Check cache for GET requests
    if (!options.method || options.method === 'GET') {
      const cached = apiCache.get(requestKey);
      if (cached) return cached;
    }

    const requestPromise = super.request<T>(endpoint, options);
    this.requestQueue.set(requestKey, requestPromise);

    try {
      const result = await requestPromise;
      
      // Cache successful GET requests
      if (!options.method || options.method === 'GET') {
        apiCache.set(requestKey, result);
      }

      return result;
    } finally {
      this.requestQueue.delete(requestKey);
    }
  }
}
```

## Deployment Integration

### 13. Environment Configuration
```bash
# frontend/.env.production
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_WS_URL=https://ws.yourdomain.com
REACT_APP_ENV=production

# frontend/.env.development
REACT_APP_API_URL=http://localhost:5000
REACT_APP_WS_URL=http://localhost:5000
REACT_APP_ENV=development
```

```python
# backend/config.py
import os

class Config:
    FRONTEND_URLS = os.environ.get('FRONTEND_URLS', 'http://localhost:3000').split(',')
    API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:5000')

class ProductionConfig(Config):
    FRONTEND_URLS = ['https://yourdomain.com']
    API_BASE_URL = 'https://api.yourdomain.com'
```

### 14. Build Integration
```json
// package.json scripts for coordinated builds
{
  "scripts": {
    "build:frontend": "cd frontend && npm run build",
    "build:backend": "cd backend && python -m build",
    "build:all": "npm run build:frontend && npm run build:backend",
    "dev:frontend": "cd frontend && npm start",
    "dev:backend": "cd backend && python app.py",
    "dev": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\""
  }
}
```

## Quality Checklist

Before deploying full stack integration, ensure:
- [ ] API contracts are documented and followed consistently
- [ ] Error handling is comprehensive across frontend and backend
- [ ] Authentication and authorization work seamlessly
- [ ] CORS is properly configured for all environments
- [ ] Real-time features work reliably with proper reconnection
- [ ] State management handles API responses correctly
- [ ] Caching strategy optimizes performance without stale data
- [ ] Integration tests cover critical user workflows
- [ ] Environment configuration is secure and appropriate
- [ ] Build and deployment processes are automated
- [ ] Performance monitoring is in place for both frontend and backend
- [ ] Security best practices are implemented throughout the stack
