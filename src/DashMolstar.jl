
module DashMolstar
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "1.3.0"

include("jl/molstarviewer.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "dash_molstar",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "rcsb-molstar.js",
    external_url = nothing,
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "dash_molstar.min.js",
    external_url = nothing,
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "dash_molstar.min.js.map",
    external_url = nothing,
    dynamic = true,
    async = nothing,
    type = :js
)
            ]
        )

    )
end
end
