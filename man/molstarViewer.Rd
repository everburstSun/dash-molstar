% Auto-generated: do not edit by hand
\name{molstarViewer}

\alias{molstarViewer}

\title{MolstarViewer component}

\description{
The Molstar viewer component for dash
}

\usage{
molstarViewer(id=NULL, camera=NULL, cameradebounce=NULL,
cameraresponddrag=NULL, className=NULL, data=NULL,
focus=NULL, frame=NULL, hover=NULL, layout=NULL,
measurement=NULL, screenshot=NULL, selection=NULL,
style=NULL, updatefocusonframechange=NULL,
updateselectiononframechange=NULL)
}

\arguments{
\item{id}{Character. The ID used to identify this component in Dash callbacks.}

\item{camera}{Logical | numeric | character | named list | unnamed list. The camera object in the molstar viewer.}

\item{cameradebounce}{Numeric. Debounce time in milliseconds for camera change events.
Set to 0 to disable debounce. Default is 100ms.}

\item{cameraresponddrag}{Logical. Whether to respond to drag events of the camera.
Set to false to disable camera parameter updates while dragging
with mouse keys, or scrolling.}

\item{className}{Character. The HTML property `class` for additional class names of the container of molstar viewer.}

\item{data}{Logical | numeric | character | named list | unnamed list. Data containing the structure info that should be loaded into molstar viewer, as well as some control flags.
The data can be generated with python method `parse_molecule`.}

\item{focus}{Named list. The structure region to let the camera focus on in the molstar viewer.}

\item{frame}{Numeric. The trajectory frame in the molstar viewer.}

\item{hover}{Named list. The structure region to be hovered in the molstar viewer.}

\item{layout}{Named list. The layout of the molstar viewer. Determining what controls to be displayed. 

The layout is not allowed to be changed once the component has been initialized.}

\item{measurement}{Logical | numeric | character | named list | unnamed list. The measurements in the molstar viewer.}

\item{screenshot}{Named list. The screenshot object containing the options for taking 
screenshot of the current view in molstar viewer.}

\item{selection}{Named list. The structure region to be selected in the molstar viewer.}

\item{style}{Named list. The HTML property `style` to control the appearence of the container of molstar viewer.}

\item{updatefocusonframechange}{Logical. Update focus data when frame index have changed.}

\item{updateselectiononframechange}{Logical. Update selection data when frame index have changed.}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

