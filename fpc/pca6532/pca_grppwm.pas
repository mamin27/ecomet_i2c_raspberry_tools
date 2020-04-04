unit pca_grppwm;

{$mode objfpc}{$H+}

interface

type
  TGWM = record
    value: Integer;
    perc: Real;
  end;

GWM = Array [1 .. 65] of TGWM;

function initialize_gwm () : GWM;

Implementation

//uses pca_display;

function initialize_gwm () : GWM;
var
  i: integer;
  percs: array [1..65] of Real = (0,1.6,3.1,4.7,6.3,7.8,9.4,10.9,12.5,14.1,15.6,17.2,18.8,20.3,21.9,23.4,25,26.6,28.1,
                                  29.7,31.3,32.8,34.4,35.9,37.5,39.1,40.6,42.2,43.8,45.3,46.9,48.4,50,51.6,53.1,54.7,
                                  56.3,57.8,59.4,60.9,62.5,64.1,65.6,67.2,68.8,70.3,71.9,73.4,75,76.6,78.1,79.7,81.3,
                                  82.8,84.4,85.9,87.5,89.1,90.6,92.2,93.8,95.3,96.9,98.4,110);
  values: array [1..65] of Integer = (0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,76,80,84,88,92,96,100,104,108,
                                      112,116,120,124,128,132,136,140,144,148,152,156,160,164,168,172,176,180,184,188,192,
                                      196,200,204,208,212,216,220,224,228,232,236,240,244,248,252,255);
  recs: GWM;
begin

  for i:=1 to 65 do
   begin
      recs[i].value := values[i];
      recs[i].perc := percs[i];
   end;
   result := recs;
end;

end.
