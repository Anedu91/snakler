module Main exposing (main)
import Browser
import Browser.Events


import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Json.Decode


main =
  Browser.element { init = init, view = view, update = update, subscriptions = subscriptions }
type alias Model = {
  snakePosition: List (Int, Int),
  area: Int,
  direction: Direction
  }

type Direction = Up | Down | Left | Right



init: () -> (Model, Cmd Msg)
init _ = ( { snakePosition = [(0,0)], area = 500, direction = Up }, Cmd.none )

type Msg = PressKey String

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    PressKey key ->
      case key of
        "ArrowUp" -> ({ model | direction = Up }, Cmd.none)
        "ArrowDown" -> ({ model | direction = Down }, Cmd.none)
        "ArrowLeft" -> ({ model | direction = Left }, Cmd.none)
        "ArrowRight" -> ({ model | direction = Right }, Cmd.none)
        _ -> (model, Cmd.none)



subscriptions : Model -> Sub Msg
subscriptions model = Browser.Events.onKeyDown (Json.Decode.map PressKey keyDecoder)

keyDecoder : Json.Decode.Decoder String
keyDecoder =
    Json.Decode.field "key" Json.Decode.string

view : Model -> Html Msg
view model =
    div [ class "container mx-auto h-screen place-content-center" ] [
      div [class ("bg-blue-500 mx-auto w-[" ++ String.fromInt model.area ++ "px] h-[" ++ String.fromInt model.area ++ "px]")  ] []
     ]
