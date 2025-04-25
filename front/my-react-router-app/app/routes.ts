import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    route("/login", "routes/login.tsx"),
    route("/logout", "routes/logout.tsx"),
    route("/properties", "routes/properties.tsx"),
    route("properties/:propertyId", "routes/property-detail.tsx"),
    route("/tenants", "routes/tenants.tsx"),
    route("tenants/:tenantId", "routes/tenant-detail.tsx"),
    route("/rentals", "routes/rentals.tsx"),
    route("/inventories", "routes/inventories.tsx"),
    route("/finance", "routes/finance.tsx"),

] satisfies RouteConfig;
