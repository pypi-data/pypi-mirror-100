// SPDX-FileCopyrightText: 2021 Galagic Limited, et. al. <https://galagic.com>
//
// SPDX-License-Identifier: AGPL-3.0-or-later
//
// figular generates visualisations from flexible, reusable parts
//
// For full copyright information see the AUTHORS file at the top-level
// directory of this distribution or at
// [AUTHORS](https://gitlab.com/thegalagic/figular/AUTHORS.md)
//
// This program is free software: you can redistribute it and/or modify it under
// the terms of the GNU Affero General Public License as published by the Free
// Software Foundation, either version 3 of the License, or (at your option) any
// later version.
//
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
// details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.

real magic_number = 10;

private pair get_label_size(string text, string font) {
  picture pic;
  label(pic, text, font("OT1", font, "m", "n"));
  return size(pic);
}

private pair get_max_label_size(string[] blobNames, string font) {
  pair max_label_size = (0,0);
  for(string blobName : blobNames) {
    pair size = get_label_size(blobName, font);
    if (size.x > max_label_size.x) {
      max_label_size = (size.x, max_label_size.y);
    }
    if (size.y > max_label_size.y) {
      max_label_size = (max_label_size.x, size.y);
    }
  }
  return max_label_size;
}

private real compute_radius(real degreeStep, pair max_label_size, real blob_radius) {
  // Width-wise
  real width_radius = (blob_radius + magic_number) / Sin(degreeStep/2);
  // We should actually check height-wise as well and return the larger
  // of the two.
  return width_radius;
}

private void draw_blob(picture pic, pair pos, pair max_label_size, string blobName, real blob_radius, string font) {
  fill(pic, circle(pos, blob_radius), p=gray(0.2));
  label(pic, blobName, pos, p=font("OT1", font, "m", "n") + rgb(0.9,0.9,0.9));
}

void draw_circle(picture pic, string[] blobNames, real degreeStart=0, bool middle=false, string font) {
  pair max_label_size = get_max_label_size(blobNames, font);
  real blob_radius = max_label_size.x/2 + magic_number;
  if(middle) {
    draw_blob(pic, (0,0), max_label_size, blobNames[0], blob_radius, font);
    blobNames.delete(0,0);
  }
  real degreeStep = 360 / blobNames.length;
  real radius = 0;
  if(blobNames.length > 1) {
    radius = compute_radius(degreeStep, max_label_size, blob_radius);

    if(middle && radius < (2*blob_radius)) {
      //There's a chance radius is too small to make space for middle blob
      radius = 2*blob_radius + (magic_number * 2);
    }
  }
  pair pos = rotate(-degreeStart) * (0, radius);


  for(string blobName : blobNames) {
    draw_blob(pic, pos, max_label_size, blobName, blob_radius, font);
    pos = rotate(-degreeStep) * pos;
  }
}

void run(picture pic) {
  string arg;
  string[] parts;
  string[] blobs={};
  real degreeStart=0;
  bool middle=false;
  string font = "cmr";

  while(!error(stdin)) {
    arg = stdin;
    parts = split(arg, "=");

    if(parts[0] == "blob" && parts.length > 1) {
      blobs.push(parts[1]);
    } else if(parts[0] == "degreeStart" && parts.length > 1) {
      degreeStart = (real)parts[1];
    } else if(parts[0] == "middle" && parts.length > 1) {
      middle = parts[1] == "true";
    } else if(parts[0] == "font" && parts.length > 1) {
      font = parts[1];
    }
  }
  draw_circle(pic, blobs, degreeStart, middle, font);
}
