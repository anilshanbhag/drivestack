#!/usr/bin/python
#
# Copyright (C) 2012 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'afshar@google.com (Ali Afshar)'

# Add the library location to the path
import sys
sys.path.insert(0, 'lib')

import os
import httplib2
from google_app.apiclient.discovery import build
from google_app.apiclient.http import MediaUpload
from google_app.oauth2client.client import flow_from_clientsecrets
from google_app.oauth2client.client import FlowExchangeError
from google_app.oauth2client.client import AccessTokenRefreshError
ALL_SCOPES = ('https://www.googleapis.com/auth/drive.file '
              'https://www.googleapis.com/auth/userinfo.email '
              'https://www.googleapis.com/auth/userinfo.profile')

class ServiceHandler():
  """Web handler for the service to read and write to Drive."""

  def post(self,service,mime_type,content,title,description):
    """Called when HTTP POST requests are received by the web application.

    The POST body is JSON which is deserialized and used as values to create a
    new file in Drive. The authorization access token for this action is
    retreived from the data store.
    """
    # Create a Drive service
    #service = self.CreateDrive()
    if service is None:
      return

    # Load the data that has been posted as JSON
    #data = self.RequestJSON()

    # Create a new file data structure.
    resource = {
      'title': title,
      'description': description,
      'mimeType': mime_type,
    }
    try:
      # Make an insert request to create a new file. A MediaInMemoryUpload
      # instance is used to upload the file body.
      resource = service.files().insert(
          body=resource,
          media_body=MediaInMemoryUpload(
              content,
              mime_type,
              resumable=True)
      ).execute()
      # Respond with the new file id as JSON.
      return str(resource['id'])
    except AccessTokenRefreshError:
      # In cases where the access token has expired and cannot be refreshed
      # (e.g. manual token revoking) redirect the user to the authorization page
      # to authorize.
      return str("error")

  def get(self,service,file_id):
    """Called when HTTP GET requests are received by the web application.

    Use the query parameter file_id to fetch the required file's metadata then
    content and return it as a JSON object.

    Since DrEdit deals with text files, it is safe to dump the content directly
    into JSON, but this is not the case with binary files, where something like
    Base64 encoding is more appropriate.
    """
    # Create a Drive service
    #service = self.CreateDrive()
    if service is None:
      return
    try:
      # Requests are expected to pass the file_id query parameter.
      #file_id = self.request.get('file_id')
      if file_id:
        # Fetch the file metadata by making the service.files().get method of
        # the Drive API.
        f = service.files().get(fileId=file_id).execute()
        downloadUrl = f.get('downloadUrl')
        # If a download URL is provided in the file metadata, use it to make an
        # authorized request to fetch the file ontent. Set this content in the
        # data to return as the 'content' field. If there is no downloadUrl,
        # just set empty content.
        if downloadUrl:
          resp, f['content'] = service._http.request(downloadUrl)
        else:
          f['content'] = ''
      else:
        f = None
      # Generate a JSON response with the file data and return to the client.
      return str(f)
    except AccessTokenRefreshError:
      # Catch AccessTokenRefreshError which occurs when the API client library
      # fails to refresh a token. This occurs, for example, when a refresh token
      # is revoked. When this happens the user is redirected to the
      # Authorization URL.
      return str(self.RedirectAuth())

  def put(self):
    """Called when HTTP PUT requests are received by the web application.

    The PUT body is JSON which is deserialized and used as values to update
    a file in Drive. The authorization access token for this action is
    retreived from the data store.
    """
    # Create a Drive service
    service = self.CreateDrive()
    if service is None:
      return
    # Load the data that has been posted as JSON
    data = self.RequestJSON()
    try:
      # Create a new file data structure.
      content = data.get('content')
      if 'content' in data:
        data.pop('content')
      if content is not None:
        # Make an update request to update the file. A MediaInMemoryUpload
        # instance is used to upload the file body. Because of a limitation, this
        # request must be made in two parts, the first to update the metadata, and
        # the second to update the body.
        resource = service.files().update(
            fileId=data['resource_id'],
            newRevision=self.request.get('newRevision', False),
            body=data,
            media_body=MediaInMemoryUpload(
                content, data['mimeType'], resumable=True)
            ).execute()
      else:
        # Only update the metadata, a patch request is prefered but not yet
        # supported on Google App Engine; see
        # http://code.google.com/p/googleappengine/issues/detail?id=6316.
        resource = service.files().update(
            fileId=data['resource_id'],
            newRevision=self.request.get('newRevision', False),
            body=data).execute()
      # Respond with the new file id as JSON.
      self.RespondJSON(resource['id'])
    except AccessTokenRefreshError:
      # In cases where the access token has expired and cannot be refreshed
      # (e.g. manual token revoking) redirect the user to the authorization page
      # to authorize.
      self.RedirectAuth()

  def RequestJSON(self):
    """Load the request body as JSON.

    Returns:
      Request body loaded as JSON or None if there is no request body.
    """
    if self.request.body:
      return json.loads(self.request.body)


class MediaInMemoryUpload(MediaUpload):
  """MediaUpload for a chunk of bytes.

  Construct a MediaFileUpload and pass as the media_body parameter of the
  method. For example, if we had a service that allowed plain text:
  """

  def __init__(self, body, mimetype='application/octet-stream',
               chunksize=256*1024, resumable=False):
    """Create a new MediaBytesUpload.

    Args:
      body: string, Bytes of body content.
      mimetype: string, Mime-type of the file or default of
        'application/octet-stream'.
      chunksize: int, File will be uploaded in chunks of this many bytes. Only
        used if resumable=True.
      resumable: bool, True if this is a resumable upload. False means upload
        in a single request.
    """
    self._body = body
    self._mimetype = mimetype
    self._resumable = resumable
    self._chunksize = chunksize

  def chunksize(self):
    """Chunk size for resumable uploads.

    Returns:
      Chunk size in bytes.
    """
    return self._chunksize

  def mimetype(self):
    """Mime type of the body.

    Returns:
      Mime type.
    """
    return self._mimetype

  def size(self):
    """Size of upload.

    Returns:
      Size of the body.
    """
    return len(self._body)

  def resumable(self):
    """Whether this upload is resumable.

    Returns:
      True if resumable upload or False.
    """
    return self._resumable

  def getbytes(self, begin, length):
    """Get bytes from the media.

    Args:
      begin: int, offset from beginning of file.
      length: int, number of bytes to read, starting at begin.

    Returns:
      A string of bytes read. May be shorter than length if EOF was reached
      first.
    """
    return self._body[begin:begin + length]

