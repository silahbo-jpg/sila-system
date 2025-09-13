import React from 'react';
import { Card, Table, Button, Space, Input, Select, Tag } from 'antd';
import { SearchOutlined, UserAddOutlined } from '@ant-design/icons';

const { Search } = Input;
const { Option } = Select;

const Users: React.FC = () => {
  // Mock data - replace with real API call
  const users = [
    {
      id: '1',
      name: 'Admin User',
      email: 'postgres',
      role: 'admin',
      status: 'active',
      lastLogin: '2023-06-15T10:30:00Z',
    },
    // Add more mock users as needed
  ];

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: 'Role',
      dataIndex: 'role',
      key: 'role',
      render: (role: string) => (
        <Tag color={role === 'admin' ? 'red' : role === 'manager' ? 'blue' : 'green'}>
          {role.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'active' ? 'green' : 'red'}>{status.toUpperCase()}</Tag>
      ),
    },
    {
      title: 'Last Login',
      dataIndex: 'lastLogin',
      key: 'lastLogin',
      render: (date: string) => new Date(date).toLocaleString(),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: any) => (
        <Space size="middle">
          <Button size="small">Edit</Button>
          <Button size="small" danger>Delete</Button>
        </Space>
      ),
    },
  ];

  return (
    <div className="p-4">
      <Card 
        title="User Management" 
        extra={
          <Button type="primary" icon={<UserAddOutlined />}>
            Add User
          </Button>
        }
      >
        <div className="mb-4 flex justify-between">
          <Search
            placeholder="Search users..."
            allowClear
            enterButton={<SearchOutlined />}
            className="w-64"
          />
          <Select defaultValue="all" style={{ width: 120 }}>
            <Option value="all">All Roles</Option>
            <Option value="admin">Admin</Option>
            <Option value="manager">Manager</Option>
            <Option value="auditor">Auditor</Option>
          </Select>
        </div>
        
        <Table 
          columns={columns} 
          dataSource={users} 
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </Card>
    </div>
  );
};

export default Users;

