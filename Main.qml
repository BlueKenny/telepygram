import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2

ApplicationWindow {
    id: mainWindow
    height: 2000
    width: 2000
    title: qsTr("Telepygram")


    Item {
        id: vars
        property string testString: ""
    }

    function changeFrame(frameSelect) {
        if (frameSelect === "Phone") {
            view.push(framePhoneNumber)
        }
        if (frameSelect === "Code") {
            view.push(framePhoneCode)
        }
        if (frameSelect === "Dialogs") {
            view.push(frameDialogs)
        }
    }

    function busy(status) {
        busyindicator.visible = status
    }

    BusyIndicator {
        id: busyindicator
        running: true //image.status === Image.Loadings
        x: mainWindow.width / 2
        y: mainWindow.height / 2
    }

    StackView {
        id: view

        delegate: StackViewDelegate {

            function transitionFinished(properties)
            {
                properties.exitItem.opacity = 1
            }

            pushTransition: StackViewTransition {
                PropertyAnimation {
                    target: enterItem
                    property: "opacity"
                    from: 0
                    to: 1
                    duration: 300
                }
                PropertyAnimation {
                    target: exitItem
                    property: "opacity"
                    from: 1
                    to: 0
                    duration: 300
                }
            }
        }

        initialItem: frameDialogs
        anchors.fill: parent

        Component {
            id: frameDialogs
            Dialogs {}
        }

        Component {
            id: framePhoneNumber
            PhoneNumber {}
        }

        Component {
            id: framePhoneCode
            PhoneCode {}
        }
    }

    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('./'));
            importModule('Main', function () {});

            //call('Main.main.phone', [], function (boolStatus) {vars.isPhone = boolStatus});
            setHandler("busy", busy);
            setHandler("changeFrame", changeFrame);
        }
    }
}
