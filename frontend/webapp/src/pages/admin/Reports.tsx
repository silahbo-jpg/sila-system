import React, { useState, useEffect } from 'react';
import { Card, Button, Row, Col, DatePicker, Spin, message } from 'antd';
import { DownloadOutlined } from '@ant-design/icons';
import { Line } from '@ant-design/charts';
import dayjs from 'dayjs';
// import { fetchDashboardStats } from '../../services/api'; // Removido: função inexistente


const { RangePicker } = DatePicker;

const Reports: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState([
    dayjs().startOf('month'),
    dayjs().endOf('day'),
  ]);
  const [chartData, setChartData] = useState([]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [start, end] = dateRange;
      // fetchDashboardStats removido, use dados vazios temporariamente
      setChartData([]);
    } catch (error) {
      message.error('Erro ao carregar dados');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [dateRange]);

  const handleExport = async () => {
    try {
      const [start, end] = dateRange;
      const response = await fetch(
        `/api/v2/dashboard/export?start=${start.format('YYYY-MM-DD')}&end=${end.format('YYYY-MM-DD')}`,
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      );
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `relatorio-${dayjs().format('YYYY-MM-DD')}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      message.error('Erro ao exportar relatório');
    }
  };

  const config = {
    data: chartData,
    xField: 'date',
    yField: 'value',
    seriesField: 'type',
    color: ['#1890ff', '#52c41a', '#faad14'],
  };

  return (
    <div className="p-4">
      <Card>
        <Row gutter={16} className="mb-6">
          <Col span={16}>
            <div className="mb-2 text-sm font-medium">Período</div>
            <RangePicker
              value={dateRange as any}
              onChange={(dates) => setDateRange(dates as any)}
              style={{ width: '100%' }}
              disabledDate={(current) => current > dayjs().endOf('day')}
            />
          </Col>
          <Col span={8} className="flex items-end">
            <Button
              type="primary"
              icon={<DownloadOutlined />}
              onClick={handleExport}
              className="w-full"
              loading={loading}
            >
              Exportar PDF
            </Button>
          </Col>
        </Row>

        <Spin spinning={loading}>
          <div className="h-96">
            <Line {...config} />
          </div>
        </Spin>
      </Card>
    </div>
  );
};

export default Reports;

