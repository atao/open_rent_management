import { Form } from "react-router";
import Button from "./button";

interface HeaderProps {
  userId?: string; // Allow userId to be undefined
}

export default function Header(prop: HeaderProps) {
  return (
    <header className="bg-gray-800 text-white p-4 flex justify-between items-center">
      <nav className="container mx-auto">
        <h1 className="text-2xl">Rental Manager</h1>
      </nav>
      <nav className="container mx-auto flex justify-end">
        {prop?.userId ? (
          <Form action="/logout" method="post">
            <Button
              type="submit"
              className="border rounded px-2.5 py-1"
              label="Logout"
            />
          </Form>
        ) : null}
      </nav>
    </header>
  );
}