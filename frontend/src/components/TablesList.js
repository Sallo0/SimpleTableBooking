import React, {useContext, useEffect, useState} from "react";
import {TableType, Table} from "./Table";
import {UserContext} from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";
import {deleteOrderApi, createOrderApi, getTablesApi, getUserOrdersApi, getAllOrdersApi} from "../api/api"

let tablesCache = null

export const TablesList = () => {
    const [token] = useContext(UserContext);
    const [errorMessage, setErrorMessage] = useState("");
    const [tables, setTables] = React.useState([]);

    useEffect(() => {
        getTables();
    }, []);

    const getUserOrders = async () => {
        const response = await getUserOrdersApi(token)
        if (!response.ok) {
            setErrorMessage("Something went wrong ");
        }
        return response.json();
    };

    const getAllOrders = async () => {
        const response = await getAllOrdersApi()
        if (!response.ok) {
            setErrorMessage("Something went wrong ");
        }
        return response.json();
    };

    const getTablesRaw = async () => {
        if (!tablesCache) {
            const response = await getTablesApi()
            if (!response.ok) {
                setErrorMessage("Something went wrong ");
            }
            tablesCache = response.json();
        }
        return tablesCache
    }

    const handleClick = async (tableId, tableNumber, type) => {
        let response
        if (type === TableType.free) {
            response = await createOrderApi(token, tableId, tableNumber)
            alert("Стол забронирован")
        }

        if (type === TableType.owned) {
            response = await deleteOrderApi(token, tableId, tableNumber)
            alert("Бронь снята")
        }

        if (!response.ok) {
            setErrorMessage("Something went wrong ");
        }

        await getTables()
    };

    const getTables = async () => {
        const [tablesRaw, userOrders, allOrders] = await Promise.all([getTablesRaw(), getUserOrders(), getAllOrders()])
        const allOrderedTables = allOrders.map((order) => order.table_id)
        const userOrderedTables = userOrders.map((order) => order.table_id)
        const tables = tablesRaw.map((table) => {
            const container = {}
            container.onClick = handleClick

            container.type = TableType.free
            if (allOrderedTables.includes(table.id)) {
                container.type = TableType.occupied
            }
            if (userOrderedTables.includes(table.id)) {
                container.type = TableType.owned
            }

            container.tableId = table.id
            container.tableNumber = table.number
            return container
        })
        setTables(tables)
    }

    return (
        <>
            <div
                className="has-text-centered-desktop columns is-multiline is-centered m-4"
            >
                {tables.map((table) => <Table key={table.tableId} {...table} />)}
            </div>

        </>)
};
