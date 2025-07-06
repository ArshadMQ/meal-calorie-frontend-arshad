"use client";

import * as React from "react";
import { toast } from "sonner";
import axios from "axios";
import { ColumnDef, ColumnFiltersState, flexRender, getCoreRowModel, getFilteredRowModel, getPaginationRowModel, getSortedRowModel, SortingState, useReactTable, VisibilityState } from "@tanstack/react-table";
import { ArrowUpDown, ChevronDown, MoreHorizontal } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { DropdownMenu, DropdownMenuCheckboxItem, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import api from "@/lib/axios";
import { getUserFromServer } from "@/lib/auth";

export type Dish = {
  dish_name: string;
  servings: number;
  calories_per_serving: number;
  total_calories: number;
  source: string;
  created_at: string;
  updated_at: string;
};

export const columns: ColumnDef<Dish>[] = [
  {
    accessorKey: "dish_name",
    header: "Dish Name",
    cell: ({ row }) => <div className="capitalize w-80">{row.getValue("dish_name")}</div>,
  },
  {
    accessorKey: "servings",
    header: "Servings",
    cell: ({ row }) => <div>{row.getValue("servings")}</div>,
  },
  {
    accessorKey: "total_calories",
    header: "Total Calories",
    cell: ({ row }) => <div className="font-medium">{row.getValue("total_calories")}</div>,
  },
  //   {
  //     accessorKey: "source",
  //     header: "Source",
  //     cell: ({ row }) => <div>{row.getValue("source")}</div>,
  //   },
  {
    accessorKey: "created_at",
    header: "Date",
    cell: ({ row }) => {
      const date = new Date(row.getValue("created_at"));
      const formatted = `${date.getDate().toString().padStart(2, "0")}-${(date.getMonth() + 1).toString().padStart(2, "0")}-${date.getFullYear()}`;
      return <div>{formatted}</div>;
    },
  },
];

export function DishTable({ user, nutritionData }: { user: any; nutritionData: any }) {
  const [data, setData] = React.useState<Dish[]>([]);
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([]);
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({});
  const [rowSelection, setRowSelection] = React.useState({});

  React.useEffect(() => {
    (async () => {
      try {
        const response = await api.get("/list-calories", {
          headers: {
            Authorizations: `Bearer ${user?.token}`,
            "Content-Type": "application/json",
          },
        });

        setData(response?.data?.data);
      } catch (error) {
        console.error("Error fetching calories data:", error);
        toast.error("Failed to fetch calories data. Please try again later.");
      }
    })();
  }, [user, nutritionData]);

  const table = useReactTable({
    data,
    columns,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      rowSelection,
    },
  });

  return (
    <div className="border mt-5 rounded-md">
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map((headerGroup) => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map((header) => {
                return <TableHead key={header.id}>{header.isPlaceholder ? null : flexRender(header.column.columnDef.header, header.getContext())}</TableHead>;
              })}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody className="overflow-y-auto max-h-[500px]">
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map((row) => (
              <TableRow key={row.id} data-state={row.getIsSelected() && "selected"}>
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={columns.length} className="h-24 text-center">
                No results.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}
