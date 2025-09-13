import React from 'react';
import { Card, Table, Tag, Space, Button, Select, Input } from 'antd';
import { SearchOutlined, FilterOutlined } from '@ant-design/icons';

const { Search } = Input;
const { Option } = Select;

const Requests: React.FC = () => {
  // Mock data - replace with real API call
  const requests = [
    {
      id: 'REQ-001',
      type: 'Certidão de Residência',
      status: 'pending',
      requester: 'John Doe',
      date: '2023-06-15T14:30:00Z',
      priority: 'high',
    },
    // Add more mock requests as needed
  ];

  const columns = [
    {
      title: 'Request ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Type',
      dataIndex: 'type',
      key: 'type',
    },
    {
      title: 'Requester',
      dataIndex: 'requester',
      key: 'requester',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        let color = 'default';
        if (status === 'completed') color = 'green';
        if (status === 'pending') color = 'orange';
        if (status === 'rejected') color = 'red';
        return <Tag color={color}>{status.toUpperCase()}</Tag>;
      },
    },
    {
      title: 'Priority',
      dataIndex: 'priority',
      key: 'priority',
      render: (priority: string) => {
        let color = 'default';
        if (priority === 'high') color = 'red';
        if (priority === 'medium') color = 'orange';
        if (priority === 'low') color = 'green';
        return <Tag color={color}>{priority.toUpperCase()}</Tag>;
      },
    },
    {
      title: 'Date',
      dataIndex: 'date',
      key: 'date',
      render: (date: string) => new Date(date).toLocaleDateString(),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: any) => (
        <Space size="middle">
          <Button size="small">View</Button>
          <Button size="small" type="primary">Process</Button>
        </Space>
      ),
    },
  ];

  return (
    <div className="p-4">
      <Card title="Service Requests">
        <div className="mb-4 flex justify-between flex-wrap gap-4">
          <Search
            placeholder="Search requests..."
            allowClear
            enterButton={<SearchOutlined />}
            className="w-64"
          />
          <div className="flex gap-2">
            <Select defaultValue="all" style={{ width: 150 }}>
              <Option value="all">All Status</Option>
              <Option value="pending">Pending</Option>
              <Option value="in-progress">In Progress</Option>
              <Option value="completed">Completed</Option>
              <Option value="rejected">Rejected</Option>
            </Select>
            <Select defaultValue="all" style={{ width: 150 }}>
              <Option value="all">All Priorities</Option>
              <Option value="high">High</Option>
              <Option value="medium">Medium</Option>
              <Option value="low">Low</Option>
            </Select>
            <Button icon={<FilterOutlined />}>More Filters</Button>
          </div>
        </div>
        
        <Table 
          columns={columns} 
          dataSource={requests} 
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </Card>
    </div>
  );
};

export default Requests;

