import React from "react";

export const TableType = {
    free: "free",
    occupied: "occupied",
    owned: "owned"
};

export const Table = ({type, tableId, tableNumber, onClick}) => {
    const handleClick = (event) => {
        onClick(tableId, tableNumber, type);
        event.target.className = buttonColor() + " is-loading"
    };


    const buttonColor = () =>{
        const res = " is-large m-2 p-10"
        if (type === TableType.owned){
            return "button has-background-success" + res
        }
        if(type === TableType.free)
            return "button" + res
        return "button has-background-grey" + res
    }

    return (
        <button
            className={buttonColor()}
            disabled={type === TableType.occupied}
            onClick={handleClick}
        >
            {tableNumber}
        </button>
    );
};


