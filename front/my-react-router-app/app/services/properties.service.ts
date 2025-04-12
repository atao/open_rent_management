import axiosInstance from "./axios.service";
import { getUserTokenInformation } from "./session.service";


export async function getProperties(request: Request) {
    const tokenInfo = await getUserTokenInformation(request);
    return (await axiosInstance.get('/properties', {
        headers: { 'Authorization': `Bearer ${tokenInfo?.token}` },
        withCredentials: true
    })
    .then(response => {
        console.log("propertie:", response.data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      }));
}

