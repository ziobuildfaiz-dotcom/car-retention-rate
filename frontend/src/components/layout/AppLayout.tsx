import { Outlet, useNavigate, useLocation } from "react-router-dom";
import { Layout, Menu } from "antd";
import {
  DashboardOutlined,
  CarOutlined,
  SwapOutlined,
  CompassOutlined,
} from "@ant-design/icons";

const { Header, Content } = Layout;

const menuItems = [
  { key: "/", icon: <DashboardOutlined />, label: "仪表盘" },
  { key: "/compare", icon: <SwapOutlined />, label: "车型对比" },
  { key: "/explore", icon: <CompassOutlined />, label: "数据探索" },
];

export default function AppLayout() {
  const navigate = useNavigate();
  const location = useLocation();

  const selectedKey = menuItems
    .filter((item) => location.pathname === item.key || (item.key !== "/" && location.pathname.startsWith(item.key)))
    .map((item) => item.key);

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          background: "#001529",
          padding: "0 24px",
          position: "sticky",
          top: 0,
          zIndex: 100,
        }}
      >
        <div
          style={{ color: "#fff", fontSize: 18, fontWeight: 600, cursor: "pointer", display: "flex", alignItems: "center", gap: 8 }}
          onClick={() => navigate("/")}
        >
          <CarOutlined />
          汽车保值率可视化平台
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={selectedKey}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
          style={{ flex: 1, justifyContent: "flex-end", minWidth: 0 }}
        />
      </Header>
      <Content style={{ padding: "24px", maxWidth: 1400, margin: "0 auto", width: "100%" }}>
        <Outlet />
      </Content>
    </Layout>
  );
}
