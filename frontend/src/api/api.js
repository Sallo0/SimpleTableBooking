export const deleteOrderApi = async (token, tableId, tableNumber) => {
    const requestOptions = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
        },
        body: JSON.stringify({
            id: tableId,
            number: tableNumber
        }),
    };
    return await fetch("/api/orders", requestOptions);
}

export const createOrderApi = async (token, tableId, tableNumber) => {
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
        },
        body: JSON.stringify({
            id: tableId,
            number: tableNumber
        }),
    };
    return await fetch("/api/orders", requestOptions);
}

export const getUserOrdersApi = async (token) => {
    const requestOptions = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
        }
    };
    return await fetch("/api/orders", requestOptions);
}

export const getAllOrdersApi = async () => {
    const requestOptions = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    };
    return await fetch("/api/orders/all", requestOptions);
}

export const getTablesApi = async () =>{
    const requestOptions = {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    };
    return await fetch("/api/tables", requestOptions);
}