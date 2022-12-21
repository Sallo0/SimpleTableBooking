import React, {useContext, useEffect, useState} from "react";

import {UserContext} from "../context/UserContext";

const Header = ({title}) => {
    const [token, setToken] = useContext(UserContext);
    const [user, setUser] = useState("")

    const handleLogout = () => {
        setToken(null);
    };


    return (
        <section className="hero is-primary is-half">
            <div className="hero-body has-text-centered m-4">
                <h1 className="title">{title}</h1>
                {token && (
                    <button className="button" onClick={handleLogout}>
                        Logout
                    </button>
                )}
            </div>
        </section>
    );
};

export default Header;