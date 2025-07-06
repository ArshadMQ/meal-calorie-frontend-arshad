import Navbar from "@/components/Navbar";
import React from "react";

const DashboardLayout = ({ children }: { children: React.ReactElement }) => {
  return (
    <>
      <div>
        <Navbar />
      </div>
      {children}
    </>
  );
};

export default DashboardLayout;
