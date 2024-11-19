module Main exposing (main)
import Browser
import Browser.Events


import Html exposing (Html, div)
import Html.Attributes exposing (class)
import Json.Decode


main =
  Browser.element { init = init, view = view, update = update, subscriptions = subscriptions }
type alias Model = {
  snakePosition: (Int, Int),
  area: Int,
  direction: Direction
  }

type Direction = Up | Down | Left | Right



init: () -> (Model, Cmd Msg)
init _ = ( { snakePosition = (0,0), area = 500, direction = Up }, Cmd.none )

type Msg = PressKey String

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    PressKey key ->
      case key of
        "ArrowUp" -> (moveSnake { model | direction = Up }, Cmd.none)
        "ArrowDown" -> (moveSnake { model | direction = Down }, Cmd.none)
        "ArrowLeft" -> (moveSnake { model | direction = Left }, Cmd.none)
        "ArrowRight" -> (moveSnake { model | direction = Right }, Cmd.none)
        _ -> (model, Cmd.none)


moveSnake : Model -> Model
moveSnake model =
  let
    (x, y) = model.snakePosition
    newPosition = case model.direction of
      Up -> (x, max 0 (y - 1))
      Down -> (x, min (model.area - 1) (y + 1))
      Left -> (max 0 (x - 1), y)
      Right -> (min (model.area - 1) (x + 1), y)
  in
  {model | snakePosition = newPosition}

subscriptions : Model -> Sub Msg
subscriptions model = Browser.Events.onKeyDown (Json.Decode.map PressKey keyDecoder)

keyDecoder : Json.Decode.Decoder String
keyDecoder =
    Json.Decode.field "key" Json.Decode.string

view : Model -> Html Msg
view model =
    div [ class "container mx-auto h-screen place-content-center" ] [
      div [class ("bg-blue-500 mx-auto relative w-[" ++ String.fromInt model.area ++ "px] h-[" ++ String.fromInt model.area ++ "px]")  ] [
        div [class ("absolute top-[" ++ String.fromInt (Tuple.second model.snakePosition) ++ "px] left-[" ++ String.fromInt (Tuple.first model.snakePosition) ++ "px] w-10 h-10 bg-red-500") ] []
      ]

     ]
