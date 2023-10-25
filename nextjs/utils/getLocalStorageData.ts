export const getLocalStorageData = (key: string) => {
    const localStorageData = localStorage.getItem(key);
    if (localStorageData) {
        return JSON.parse(localStorageData);
    }
    return null;
};

export const getAuthorization = () => {
    const token = localStorage.getItem("token");
    const tokenType = localStorage.getItem("tokenType");
    if (token) {
        return {
            Authorization: `${tokenType} ${token}`,
        }
    }
    return null;

}