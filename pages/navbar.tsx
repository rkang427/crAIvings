"use client";

import { Button } from "../components/ui/button";
import { GitIcon, VercelIcon } from "../components/icons";
import Link from "next/link";

// Make sure to use default export
const Navbar = () => {
  return (
    <div className="p-2 flex flex-row gap-2 justify-between">
      <Link href="https://github.com/rkang427/crAIvings">
        <Button variant="outline">
          <GitIcon /> View Source Code
        </Button>
      </Link>
    </div>
  );
};

export default Navbar; // Default export
