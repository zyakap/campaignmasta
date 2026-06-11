package com.campaignmasta.data.local.dao;

import android.database.Cursor;
import android.os.CancellationSignal;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.room.CoroutinesRoom;
import androidx.room.EntityInsertionAdapter;
import androidx.room.RoomDatabase;
import androidx.room.RoomSQLiteQuery;
import androidx.room.SharedSQLiteStatement;
import androidx.room.util.CursorUtil;
import androidx.room.util.DBUtil;
import androidx.sqlite.db.SupportSQLiteStatement;
import com.campaignmasta.data.local.entity.MessageEntity;
import java.lang.Class;
import java.lang.Exception;
import java.lang.Integer;
import java.lang.Object;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import javax.annotation.processing.Generated;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlinx.coroutines.flow.Flow;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class MessageDao_Impl implements MessageDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<MessageEntity> __insertionAdapterOfMessageEntity;

  private final SharedSQLiteStatement __preparedStmtOfMarkRead;

  private final SharedSQLiteStatement __preparedStmtOfMarkAcknowledged;

  private final SharedSQLiteStatement __preparedStmtOfMarkReadSynced;

  private final SharedSQLiteStatement __preparedStmtOfMarkAckSynced;

  public MessageDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfMessageEntity = new EntityInsertionAdapter<MessageEntity>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `messages` (`localId`,`serverId`,`subject`,`body`,`messageType`,`priority`,`senderName`,`deliveryChannel`,`status`,`sentAt`,`isRead`,`isAcknowledged`,`readReceiptRequired`,`acknowledgementRequired`,`updatedAt`,`readSyncStatus`,`ackSyncStatus`) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final MessageEntity entity) {
        statement.bindString(1, entity.getLocalId());
        if (entity.getServerId() == null) {
          statement.bindNull(2);
        } else {
          statement.bindLong(2, entity.getServerId());
        }
        statement.bindString(3, entity.getSubject());
        statement.bindString(4, entity.getBody());
        statement.bindString(5, entity.getMessageType());
        statement.bindString(6, entity.getPriority());
        statement.bindString(7, entity.getSenderName());
        statement.bindString(8, entity.getDeliveryChannel());
        statement.bindString(9, entity.getStatus());
        if (entity.getSentAt() == null) {
          statement.bindNull(10);
        } else {
          statement.bindString(10, entity.getSentAt());
        }
        final int _tmp = entity.isRead() ? 1 : 0;
        statement.bindLong(11, _tmp);
        final int _tmp_1 = entity.isAcknowledged() ? 1 : 0;
        statement.bindLong(12, _tmp_1);
        final int _tmp_2 = entity.getReadReceiptRequired() ? 1 : 0;
        statement.bindLong(13, _tmp_2);
        final int _tmp_3 = entity.getAcknowledgementRequired() ? 1 : 0;
        statement.bindLong(14, _tmp_3);
        statement.bindString(15, entity.getUpdatedAt());
        statement.bindString(16, entity.getReadSyncStatus());
        statement.bindString(17, entity.getAckSyncStatus());
      }
    };
    this.__preparedStmtOfMarkRead = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "UPDATE messages SET isRead = 1, readSyncStatus = 'PENDING' WHERE localId = ?";
        return _query;
      }
    };
    this.__preparedStmtOfMarkAcknowledged = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "UPDATE messages SET isAcknowledged = 1, ackSyncStatus = 'PENDING' WHERE localId = ?";
        return _query;
      }
    };
    this.__preparedStmtOfMarkReadSynced = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "UPDATE messages SET readSyncStatus = 'SYNCED' WHERE localId = ?";
        return _query;
      }
    };
    this.__preparedStmtOfMarkAckSynced = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "UPDATE messages SET ackSyncStatus = 'SYNCED' WHERE localId = ?";
        return _query;
      }
    };
  }

  @Override
  public Object insert(final MessageEntity entity, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __insertionAdapterOfMessageEntity.insert(entity);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object insertAll(final List<MessageEntity> entities,
      final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __insertionAdapterOfMessageEntity.insert(entities);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object markRead(final String localId, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfMarkRead.acquire();
        int _argIndex = 1;
        _stmt.bindString(_argIndex, localId);
        try {
          __db.beginTransaction();
          try {
            _stmt.executeUpdateDelete();
            __db.setTransactionSuccessful();
            return Unit.INSTANCE;
          } finally {
            __db.endTransaction();
          }
        } finally {
          __preparedStmtOfMarkRead.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Object markAcknowledged(final String localId,
      final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfMarkAcknowledged.acquire();
        int _argIndex = 1;
        _stmt.bindString(_argIndex, localId);
        try {
          __db.beginTransaction();
          try {
            _stmt.executeUpdateDelete();
            __db.setTransactionSuccessful();
            return Unit.INSTANCE;
          } finally {
            __db.endTransaction();
          }
        } finally {
          __preparedStmtOfMarkAcknowledged.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Object markReadSynced(final String localId, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfMarkReadSynced.acquire();
        int _argIndex = 1;
        _stmt.bindString(_argIndex, localId);
        try {
          __db.beginTransaction();
          try {
            _stmt.executeUpdateDelete();
            __db.setTransactionSuccessful();
            return Unit.INSTANCE;
          } finally {
            __db.endTransaction();
          }
        } finally {
          __preparedStmtOfMarkReadSynced.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Object markAckSynced(final String localId, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfMarkAckSynced.acquire();
        int _argIndex = 1;
        _stmt.bindString(_argIndex, localId);
        try {
          __db.beginTransaction();
          try {
            _stmt.executeUpdateDelete();
            __db.setTransactionSuccessful();
            return Unit.INSTANCE;
          } finally {
            __db.endTransaction();
          }
        } finally {
          __preparedStmtOfMarkAckSynced.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Flow<List<MessageEntity>> getAllFlow() {
    final String _sql = "SELECT * FROM messages ORDER BY sentAt DESC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"messages"}, new Callable<List<MessageEntity>>() {
      @Override
      @NonNull
      public List<MessageEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfSubject = CursorUtil.getColumnIndexOrThrow(_cursor, "subject");
          final int _cursorIndexOfBody = CursorUtil.getColumnIndexOrThrow(_cursor, "body");
          final int _cursorIndexOfMessageType = CursorUtil.getColumnIndexOrThrow(_cursor, "messageType");
          final int _cursorIndexOfPriority = CursorUtil.getColumnIndexOrThrow(_cursor, "priority");
          final int _cursorIndexOfSenderName = CursorUtil.getColumnIndexOrThrow(_cursor, "senderName");
          final int _cursorIndexOfDeliveryChannel = CursorUtil.getColumnIndexOrThrow(_cursor, "deliveryChannel");
          final int _cursorIndexOfStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "status");
          final int _cursorIndexOfSentAt = CursorUtil.getColumnIndexOrThrow(_cursor, "sentAt");
          final int _cursorIndexOfIsRead = CursorUtil.getColumnIndexOrThrow(_cursor, "isRead");
          final int _cursorIndexOfIsAcknowledged = CursorUtil.getColumnIndexOrThrow(_cursor, "isAcknowledged");
          final int _cursorIndexOfReadReceiptRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "readReceiptRequired");
          final int _cursorIndexOfAcknowledgementRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "acknowledgementRequired");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final int _cursorIndexOfReadSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "readSyncStatus");
          final int _cursorIndexOfAckSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "ackSyncStatus");
          final List<MessageEntity> _result = new ArrayList<MessageEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final MessageEntity _item;
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final Integer _tmpServerId;
            if (_cursor.isNull(_cursorIndexOfServerId)) {
              _tmpServerId = null;
            } else {
              _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            }
            final String _tmpSubject;
            _tmpSubject = _cursor.getString(_cursorIndexOfSubject);
            final String _tmpBody;
            _tmpBody = _cursor.getString(_cursorIndexOfBody);
            final String _tmpMessageType;
            _tmpMessageType = _cursor.getString(_cursorIndexOfMessageType);
            final String _tmpPriority;
            _tmpPriority = _cursor.getString(_cursorIndexOfPriority);
            final String _tmpSenderName;
            _tmpSenderName = _cursor.getString(_cursorIndexOfSenderName);
            final String _tmpDeliveryChannel;
            _tmpDeliveryChannel = _cursor.getString(_cursorIndexOfDeliveryChannel);
            final String _tmpStatus;
            _tmpStatus = _cursor.getString(_cursorIndexOfStatus);
            final String _tmpSentAt;
            if (_cursor.isNull(_cursorIndexOfSentAt)) {
              _tmpSentAt = null;
            } else {
              _tmpSentAt = _cursor.getString(_cursorIndexOfSentAt);
            }
            final boolean _tmpIsRead;
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfIsRead);
            _tmpIsRead = _tmp != 0;
            final boolean _tmpIsAcknowledged;
            final int _tmp_1;
            _tmp_1 = _cursor.getInt(_cursorIndexOfIsAcknowledged);
            _tmpIsAcknowledged = _tmp_1 != 0;
            final boolean _tmpReadReceiptRequired;
            final int _tmp_2;
            _tmp_2 = _cursor.getInt(_cursorIndexOfReadReceiptRequired);
            _tmpReadReceiptRequired = _tmp_2 != 0;
            final boolean _tmpAcknowledgementRequired;
            final int _tmp_3;
            _tmp_3 = _cursor.getInt(_cursorIndexOfAcknowledgementRequired);
            _tmpAcknowledgementRequired = _tmp_3 != 0;
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            final String _tmpReadSyncStatus;
            _tmpReadSyncStatus = _cursor.getString(_cursorIndexOfReadSyncStatus);
            final String _tmpAckSyncStatus;
            _tmpAckSyncStatus = _cursor.getString(_cursorIndexOfAckSyncStatus);
            _item = new MessageEntity(_tmpLocalId,_tmpServerId,_tmpSubject,_tmpBody,_tmpMessageType,_tmpPriority,_tmpSenderName,_tmpDeliveryChannel,_tmpStatus,_tmpSentAt,_tmpIsRead,_tmpIsAcknowledged,_tmpReadReceiptRequired,_tmpAcknowledgementRequired,_tmpUpdatedAt,_tmpReadSyncStatus,_tmpAckSyncStatus);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public Flow<List<MessageEntity>> getUnreadFlow() {
    final String _sql = "SELECT * FROM messages WHERE isRead = 0 ORDER BY sentAt DESC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"messages"}, new Callable<List<MessageEntity>>() {
      @Override
      @NonNull
      public List<MessageEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfSubject = CursorUtil.getColumnIndexOrThrow(_cursor, "subject");
          final int _cursorIndexOfBody = CursorUtil.getColumnIndexOrThrow(_cursor, "body");
          final int _cursorIndexOfMessageType = CursorUtil.getColumnIndexOrThrow(_cursor, "messageType");
          final int _cursorIndexOfPriority = CursorUtil.getColumnIndexOrThrow(_cursor, "priority");
          final int _cursorIndexOfSenderName = CursorUtil.getColumnIndexOrThrow(_cursor, "senderName");
          final int _cursorIndexOfDeliveryChannel = CursorUtil.getColumnIndexOrThrow(_cursor, "deliveryChannel");
          final int _cursorIndexOfStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "status");
          final int _cursorIndexOfSentAt = CursorUtil.getColumnIndexOrThrow(_cursor, "sentAt");
          final int _cursorIndexOfIsRead = CursorUtil.getColumnIndexOrThrow(_cursor, "isRead");
          final int _cursorIndexOfIsAcknowledged = CursorUtil.getColumnIndexOrThrow(_cursor, "isAcknowledged");
          final int _cursorIndexOfReadReceiptRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "readReceiptRequired");
          final int _cursorIndexOfAcknowledgementRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "acknowledgementRequired");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final int _cursorIndexOfReadSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "readSyncStatus");
          final int _cursorIndexOfAckSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "ackSyncStatus");
          final List<MessageEntity> _result = new ArrayList<MessageEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final MessageEntity _item;
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final Integer _tmpServerId;
            if (_cursor.isNull(_cursorIndexOfServerId)) {
              _tmpServerId = null;
            } else {
              _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            }
            final String _tmpSubject;
            _tmpSubject = _cursor.getString(_cursorIndexOfSubject);
            final String _tmpBody;
            _tmpBody = _cursor.getString(_cursorIndexOfBody);
            final String _tmpMessageType;
            _tmpMessageType = _cursor.getString(_cursorIndexOfMessageType);
            final String _tmpPriority;
            _tmpPriority = _cursor.getString(_cursorIndexOfPriority);
            final String _tmpSenderName;
            _tmpSenderName = _cursor.getString(_cursorIndexOfSenderName);
            final String _tmpDeliveryChannel;
            _tmpDeliveryChannel = _cursor.getString(_cursorIndexOfDeliveryChannel);
            final String _tmpStatus;
            _tmpStatus = _cursor.getString(_cursorIndexOfStatus);
            final String _tmpSentAt;
            if (_cursor.isNull(_cursorIndexOfSentAt)) {
              _tmpSentAt = null;
            } else {
              _tmpSentAt = _cursor.getString(_cursorIndexOfSentAt);
            }
            final boolean _tmpIsRead;
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfIsRead);
            _tmpIsRead = _tmp != 0;
            final boolean _tmpIsAcknowledged;
            final int _tmp_1;
            _tmp_1 = _cursor.getInt(_cursorIndexOfIsAcknowledged);
            _tmpIsAcknowledged = _tmp_1 != 0;
            final boolean _tmpReadReceiptRequired;
            final int _tmp_2;
            _tmp_2 = _cursor.getInt(_cursorIndexOfReadReceiptRequired);
            _tmpReadReceiptRequired = _tmp_2 != 0;
            final boolean _tmpAcknowledgementRequired;
            final int _tmp_3;
            _tmp_3 = _cursor.getInt(_cursorIndexOfAcknowledgementRequired);
            _tmpAcknowledgementRequired = _tmp_3 != 0;
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            final String _tmpReadSyncStatus;
            _tmpReadSyncStatus = _cursor.getString(_cursorIndexOfReadSyncStatus);
            final String _tmpAckSyncStatus;
            _tmpAckSyncStatus = _cursor.getString(_cursorIndexOfAckSyncStatus);
            _item = new MessageEntity(_tmpLocalId,_tmpServerId,_tmpSubject,_tmpBody,_tmpMessageType,_tmpPriority,_tmpSenderName,_tmpDeliveryChannel,_tmpStatus,_tmpSentAt,_tmpIsRead,_tmpIsAcknowledged,_tmpReadReceiptRequired,_tmpAcknowledgementRequired,_tmpUpdatedAt,_tmpReadSyncStatus,_tmpAckSyncStatus);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public Flow<Integer> unreadCountFlow() {
    final String _sql = "SELECT COUNT(*) FROM messages WHERE isRead = 0";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"messages"}, new Callable<Integer>() {
      @Override
      @NonNull
      public Integer call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final Integer _result;
          if (_cursor.moveToFirst()) {
            final int _tmp;
            _tmp = _cursor.getInt(0);
            _result = _tmp;
          } else {
            _result = 0;
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public Object getByLocalId(final String localId,
      final Continuation<? super MessageEntity> $completion) {
    final String _sql = "SELECT * FROM messages WHERE localId = ?";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindString(_argIndex, localId);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<MessageEntity>() {
      @Override
      @Nullable
      public MessageEntity call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfSubject = CursorUtil.getColumnIndexOrThrow(_cursor, "subject");
          final int _cursorIndexOfBody = CursorUtil.getColumnIndexOrThrow(_cursor, "body");
          final int _cursorIndexOfMessageType = CursorUtil.getColumnIndexOrThrow(_cursor, "messageType");
          final int _cursorIndexOfPriority = CursorUtil.getColumnIndexOrThrow(_cursor, "priority");
          final int _cursorIndexOfSenderName = CursorUtil.getColumnIndexOrThrow(_cursor, "senderName");
          final int _cursorIndexOfDeliveryChannel = CursorUtil.getColumnIndexOrThrow(_cursor, "deliveryChannel");
          final int _cursorIndexOfStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "status");
          final int _cursorIndexOfSentAt = CursorUtil.getColumnIndexOrThrow(_cursor, "sentAt");
          final int _cursorIndexOfIsRead = CursorUtil.getColumnIndexOrThrow(_cursor, "isRead");
          final int _cursorIndexOfIsAcknowledged = CursorUtil.getColumnIndexOrThrow(_cursor, "isAcknowledged");
          final int _cursorIndexOfReadReceiptRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "readReceiptRequired");
          final int _cursorIndexOfAcknowledgementRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "acknowledgementRequired");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final int _cursorIndexOfReadSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "readSyncStatus");
          final int _cursorIndexOfAckSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "ackSyncStatus");
          final MessageEntity _result;
          if (_cursor.moveToFirst()) {
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final Integer _tmpServerId;
            if (_cursor.isNull(_cursorIndexOfServerId)) {
              _tmpServerId = null;
            } else {
              _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            }
            final String _tmpSubject;
            _tmpSubject = _cursor.getString(_cursorIndexOfSubject);
            final String _tmpBody;
            _tmpBody = _cursor.getString(_cursorIndexOfBody);
            final String _tmpMessageType;
            _tmpMessageType = _cursor.getString(_cursorIndexOfMessageType);
            final String _tmpPriority;
            _tmpPriority = _cursor.getString(_cursorIndexOfPriority);
            final String _tmpSenderName;
            _tmpSenderName = _cursor.getString(_cursorIndexOfSenderName);
            final String _tmpDeliveryChannel;
            _tmpDeliveryChannel = _cursor.getString(_cursorIndexOfDeliveryChannel);
            final String _tmpStatus;
            _tmpStatus = _cursor.getString(_cursorIndexOfStatus);
            final String _tmpSentAt;
            if (_cursor.isNull(_cursorIndexOfSentAt)) {
              _tmpSentAt = null;
            } else {
              _tmpSentAt = _cursor.getString(_cursorIndexOfSentAt);
            }
            final boolean _tmpIsRead;
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfIsRead);
            _tmpIsRead = _tmp != 0;
            final boolean _tmpIsAcknowledged;
            final int _tmp_1;
            _tmp_1 = _cursor.getInt(_cursorIndexOfIsAcknowledged);
            _tmpIsAcknowledged = _tmp_1 != 0;
            final boolean _tmpReadReceiptRequired;
            final int _tmp_2;
            _tmp_2 = _cursor.getInt(_cursorIndexOfReadReceiptRequired);
            _tmpReadReceiptRequired = _tmp_2 != 0;
            final boolean _tmpAcknowledgementRequired;
            final int _tmp_3;
            _tmp_3 = _cursor.getInt(_cursorIndexOfAcknowledgementRequired);
            _tmpAcknowledgementRequired = _tmp_3 != 0;
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            final String _tmpReadSyncStatus;
            _tmpReadSyncStatus = _cursor.getString(_cursorIndexOfReadSyncStatus);
            final String _tmpAckSyncStatus;
            _tmpAckSyncStatus = _cursor.getString(_cursorIndexOfAckSyncStatus);
            _result = new MessageEntity(_tmpLocalId,_tmpServerId,_tmpSubject,_tmpBody,_tmpMessageType,_tmpPriority,_tmpSenderName,_tmpDeliveryChannel,_tmpStatus,_tmpSentAt,_tmpIsRead,_tmpIsAcknowledged,_tmpReadReceiptRequired,_tmpAcknowledgementRequired,_tmpUpdatedAt,_tmpReadSyncStatus,_tmpAckSyncStatus);
          } else {
            _result = null;
          }
          return _result;
        } finally {
          _cursor.close();
          _statement.release();
        }
      }
    }, $completion);
  }

  @Override
  public Object getPendingReadSync(final Continuation<? super List<MessageEntity>> $completion) {
    final String _sql = "SELECT * FROM messages WHERE readSyncStatus = 'PENDING'";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<List<MessageEntity>>() {
      @Override
      @NonNull
      public List<MessageEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfSubject = CursorUtil.getColumnIndexOrThrow(_cursor, "subject");
          final int _cursorIndexOfBody = CursorUtil.getColumnIndexOrThrow(_cursor, "body");
          final int _cursorIndexOfMessageType = CursorUtil.getColumnIndexOrThrow(_cursor, "messageType");
          final int _cursorIndexOfPriority = CursorUtil.getColumnIndexOrThrow(_cursor, "priority");
          final int _cursorIndexOfSenderName = CursorUtil.getColumnIndexOrThrow(_cursor, "senderName");
          final int _cursorIndexOfDeliveryChannel = CursorUtil.getColumnIndexOrThrow(_cursor, "deliveryChannel");
          final int _cursorIndexOfStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "status");
          final int _cursorIndexOfSentAt = CursorUtil.getColumnIndexOrThrow(_cursor, "sentAt");
          final int _cursorIndexOfIsRead = CursorUtil.getColumnIndexOrThrow(_cursor, "isRead");
          final int _cursorIndexOfIsAcknowledged = CursorUtil.getColumnIndexOrThrow(_cursor, "isAcknowledged");
          final int _cursorIndexOfReadReceiptRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "readReceiptRequired");
          final int _cursorIndexOfAcknowledgementRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "acknowledgementRequired");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final int _cursorIndexOfReadSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "readSyncStatus");
          final int _cursorIndexOfAckSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "ackSyncStatus");
          final List<MessageEntity> _result = new ArrayList<MessageEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final MessageEntity _item;
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final Integer _tmpServerId;
            if (_cursor.isNull(_cursorIndexOfServerId)) {
              _tmpServerId = null;
            } else {
              _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            }
            final String _tmpSubject;
            _tmpSubject = _cursor.getString(_cursorIndexOfSubject);
            final String _tmpBody;
            _tmpBody = _cursor.getString(_cursorIndexOfBody);
            final String _tmpMessageType;
            _tmpMessageType = _cursor.getString(_cursorIndexOfMessageType);
            final String _tmpPriority;
            _tmpPriority = _cursor.getString(_cursorIndexOfPriority);
            final String _tmpSenderName;
            _tmpSenderName = _cursor.getString(_cursorIndexOfSenderName);
            final String _tmpDeliveryChannel;
            _tmpDeliveryChannel = _cursor.getString(_cursorIndexOfDeliveryChannel);
            final String _tmpStatus;
            _tmpStatus = _cursor.getString(_cursorIndexOfStatus);
            final String _tmpSentAt;
            if (_cursor.isNull(_cursorIndexOfSentAt)) {
              _tmpSentAt = null;
            } else {
              _tmpSentAt = _cursor.getString(_cursorIndexOfSentAt);
            }
            final boolean _tmpIsRead;
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfIsRead);
            _tmpIsRead = _tmp != 0;
            final boolean _tmpIsAcknowledged;
            final int _tmp_1;
            _tmp_1 = _cursor.getInt(_cursorIndexOfIsAcknowledged);
            _tmpIsAcknowledged = _tmp_1 != 0;
            final boolean _tmpReadReceiptRequired;
            final int _tmp_2;
            _tmp_2 = _cursor.getInt(_cursorIndexOfReadReceiptRequired);
            _tmpReadReceiptRequired = _tmp_2 != 0;
            final boolean _tmpAcknowledgementRequired;
            final int _tmp_3;
            _tmp_3 = _cursor.getInt(_cursorIndexOfAcknowledgementRequired);
            _tmpAcknowledgementRequired = _tmp_3 != 0;
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            final String _tmpReadSyncStatus;
            _tmpReadSyncStatus = _cursor.getString(_cursorIndexOfReadSyncStatus);
            final String _tmpAckSyncStatus;
            _tmpAckSyncStatus = _cursor.getString(_cursorIndexOfAckSyncStatus);
            _item = new MessageEntity(_tmpLocalId,_tmpServerId,_tmpSubject,_tmpBody,_tmpMessageType,_tmpPriority,_tmpSenderName,_tmpDeliveryChannel,_tmpStatus,_tmpSentAt,_tmpIsRead,_tmpIsAcknowledged,_tmpReadReceiptRequired,_tmpAcknowledgementRequired,_tmpUpdatedAt,_tmpReadSyncStatus,_tmpAckSyncStatus);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
          _statement.release();
        }
      }
    }, $completion);
  }

  @Override
  public Object getPendingAckSync(final Continuation<? super List<MessageEntity>> $completion) {
    final String _sql = "SELECT * FROM messages WHERE ackSyncStatus = 'PENDING'";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<List<MessageEntity>>() {
      @Override
      @NonNull
      public List<MessageEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfSubject = CursorUtil.getColumnIndexOrThrow(_cursor, "subject");
          final int _cursorIndexOfBody = CursorUtil.getColumnIndexOrThrow(_cursor, "body");
          final int _cursorIndexOfMessageType = CursorUtil.getColumnIndexOrThrow(_cursor, "messageType");
          final int _cursorIndexOfPriority = CursorUtil.getColumnIndexOrThrow(_cursor, "priority");
          final int _cursorIndexOfSenderName = CursorUtil.getColumnIndexOrThrow(_cursor, "senderName");
          final int _cursorIndexOfDeliveryChannel = CursorUtil.getColumnIndexOrThrow(_cursor, "deliveryChannel");
          final int _cursorIndexOfStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "status");
          final int _cursorIndexOfSentAt = CursorUtil.getColumnIndexOrThrow(_cursor, "sentAt");
          final int _cursorIndexOfIsRead = CursorUtil.getColumnIndexOrThrow(_cursor, "isRead");
          final int _cursorIndexOfIsAcknowledged = CursorUtil.getColumnIndexOrThrow(_cursor, "isAcknowledged");
          final int _cursorIndexOfReadReceiptRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "readReceiptRequired");
          final int _cursorIndexOfAcknowledgementRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "acknowledgementRequired");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final int _cursorIndexOfReadSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "readSyncStatus");
          final int _cursorIndexOfAckSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "ackSyncStatus");
          final List<MessageEntity> _result = new ArrayList<MessageEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final MessageEntity _item;
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final Integer _tmpServerId;
            if (_cursor.isNull(_cursorIndexOfServerId)) {
              _tmpServerId = null;
            } else {
              _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            }
            final String _tmpSubject;
            _tmpSubject = _cursor.getString(_cursorIndexOfSubject);
            final String _tmpBody;
            _tmpBody = _cursor.getString(_cursorIndexOfBody);
            final String _tmpMessageType;
            _tmpMessageType = _cursor.getString(_cursorIndexOfMessageType);
            final String _tmpPriority;
            _tmpPriority = _cursor.getString(_cursorIndexOfPriority);
            final String _tmpSenderName;
            _tmpSenderName = _cursor.getString(_cursorIndexOfSenderName);
            final String _tmpDeliveryChannel;
            _tmpDeliveryChannel = _cursor.getString(_cursorIndexOfDeliveryChannel);
            final String _tmpStatus;
            _tmpStatus = _cursor.getString(_cursorIndexOfStatus);
            final String _tmpSentAt;
            if (_cursor.isNull(_cursorIndexOfSentAt)) {
              _tmpSentAt = null;
            } else {
              _tmpSentAt = _cursor.getString(_cursorIndexOfSentAt);
            }
            final boolean _tmpIsRead;
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfIsRead);
            _tmpIsRead = _tmp != 0;
            final boolean _tmpIsAcknowledged;
            final int _tmp_1;
            _tmp_1 = _cursor.getInt(_cursorIndexOfIsAcknowledged);
            _tmpIsAcknowledged = _tmp_1 != 0;
            final boolean _tmpReadReceiptRequired;
            final int _tmp_2;
            _tmp_2 = _cursor.getInt(_cursorIndexOfReadReceiptRequired);
            _tmpReadReceiptRequired = _tmp_2 != 0;
            final boolean _tmpAcknowledgementRequired;
            final int _tmp_3;
            _tmp_3 = _cursor.getInt(_cursorIndexOfAcknowledgementRequired);
            _tmpAcknowledgementRequired = _tmp_3 != 0;
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            final String _tmpReadSyncStatus;
            _tmpReadSyncStatus = _cursor.getString(_cursorIndexOfReadSyncStatus);
            final String _tmpAckSyncStatus;
            _tmpAckSyncStatus = _cursor.getString(_cursorIndexOfAckSyncStatus);
            _item = new MessageEntity(_tmpLocalId,_tmpServerId,_tmpSubject,_tmpBody,_tmpMessageType,_tmpPriority,_tmpSenderName,_tmpDeliveryChannel,_tmpStatus,_tmpSentAt,_tmpIsRead,_tmpIsAcknowledged,_tmpReadReceiptRequired,_tmpAcknowledgementRequired,_tmpUpdatedAt,_tmpReadSyncStatus,_tmpAckSyncStatus);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
          _statement.release();
        }
      }
    }, $completion);
  }

  @NonNull
  public static List<Class<?>> getRequiredConverters() {
    return Collections.emptyList();
  }
}
