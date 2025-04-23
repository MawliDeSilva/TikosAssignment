// FashionClientApp.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardContent } from "./ui/card";
import { Input } from "./ui/input";
import { motion } from "framer-motion";

const FashionClientApp = () => {
  const [fashionItems, setFashionItems] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/fashion-items")
      .then((response) => setFashionItems(response.data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  const filteredItems = fashionItems.filter(
    (item) =>
      item.name.toLowerCase().includes(search.toLowerCase()) ||
      item.brand.toLowerCase().includes(search.toLowerCase()) ||
      item.category.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-4 text-center">Fashion Catalog</h1>
      <Input
        placeholder="Search by name, brand, or category..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="mb-6"
      />
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 md:grid-cols-3">
        {filteredItems.map((item) => (
          <motion.div
            key={item.id}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Card className="rounded-2xl shadow-md">
              <CardContent className="p-4">
                <h2 className="text-xl font-semibold">{item.name}</h2>
                <p className="text-sm text-gray-600">Brand: {item.brand}</p>
                <p className="text-sm text-gray-600">Category: {item.category}</p>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default FashionClientApp;
