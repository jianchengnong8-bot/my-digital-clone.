/**
 * 前台路由组布局
 * 在根布局基础上叠加导航栏
 */
import { NavBar } from "@/components/ui/NavBar";

export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <NavBar />
      <main className="flex-1">{children}</main>
    </>
  );
}
